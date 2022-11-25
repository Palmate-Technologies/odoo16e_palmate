# -*- coding: utf-8 -*-
###################################################################################
#
#    This program is free software: you can modify
#    it under the terms of the GNU Affero General Public License (AGPL) as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
###################################################################################
from odoo import api, fields, models


class HrEmployeePrivate(models.Model):
    _inherit = 'hr.employee'

    def _read(self, fields):
        if self.check_access_rights('read', raise_exception=False):
            return super(HrEmployeePrivate, self)._read(fields)

        # HACK: retrieve publicly available values from hr.employee.public and
        # copy them to the cache of self; non-public data will be missing from
        # cache, and interpreted as an access error
        self.flush_recordset(fields)
        public = self.env['hr.employee.public'].browse(self._ids)
        public.read(fields)
        #######################################################
        fields.remove('contract_id')
        #######################################################
        for fname in fields:
            values = self.env.cache.get_values(public, public._fields[fname])
            if self._fields[fname].translate:
                values = [(value.copy() if value else None) for value in values]
            self.env.cache.update_raw(self, self._fields[fname], values)

