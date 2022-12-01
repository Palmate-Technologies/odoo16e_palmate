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
# from odoo import api, fields, models
#
#
# class HrEmployeePrivate(models.Model):
#     _inherit = 'hr.employee'

    # def name_get(self):
    #     print(666666666666666)
    #     if self.check_access_rights('read', raise_exception=False):
    #         return super(HrEmployeePrivate, self).name_get()
    #     return self.env['hr.employee.public'].browse(self.ids).name_get()


    # def _read(self, fields):
    #     if self.check_access_rights('read', raise_exception=False):
    #         return super(HrEmployeePrivate, self)._read(fields)
    #
    #     # HACK: retrieve publicly available values from hr.employee.public and
    #     # copy them to the cache of self; non-public data will be missing from
    #     # cache, and interpreted as an access error
    #     self.flush_recordset(fields)
    #     public = self.env['hr.employee.public'].browse(self._ids)
    #     public.read(fields)
    #     #######################################################
    #     print(fields)
    #     print(public)
    #     print(666666666666)
    #     # fields.remove('contract_id')
    #     #######################################################
    #     for fname in fields:
    #         values = self.env.cache.get_values(public, public._fields[fname])
    #         if self._fields[fname].translate:
    #             values = [(value.copy() if value else None) for value in values]
    #         self.env.cache.update_raw(self, self._fields[fname], values)


    # def read(self, fields, load='_classic_read'):
    #     print(666666666666)
    #     if self.check_access_rights('read', raise_exception=False):
    #         return super(HrEmployeePrivate, self).read(fields, load=load)
    #     private_fields = set(fields).difference(self.env['hr.employee.public']._fields.keys())
    #     if private_fields:
    #         raise AccessError(_('The fields "%s" you try to read is not available on the public employee profile.') % (','.join(private_fields)))
    #     return self.env['hr.employee.public'].browse(self.ids).read(fields, load=load)

    # @api.model
    # def get_view(self, view_id=None, view_type='form', **options):
    #     print(666666)
    #     if self.check_access_rights('read', raise_exception=False):
    #         return super().get_view(view_id, view_type, **options)
    #     return self.env['hr.employee.public'].get_view(view_id, view_type, **options)


    # @api.model
    # def _search(self, args, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
    #     """
    #         We override the _search because it is the method that checks the access rights
    #         This is correct to override the _search. That way we enforce the fact that calling
    #         search on an hr.employee returns a hr.employee recordset, even if you don't have access
    #         to this model, as the result of _search (the ids of the public employees) is to be
    #         browsed on the hr.employee model. This can be trusted as the ids of the public
    #         employees exactly match the ids of the related hr.employee.
    #     """
    #     print(666666666)
    #     if self.check_access_rights('read', raise_exception=False):
    #         return super(HrEmployeePrivate, self)._search(args, offset=offset, limit=limit, order=order, count=count, access_rights_uid=access_rights_uid)
    #     try:
    #         ids = self.env['hr.employee.public']._search(args, offset=offset, limit=limit, order=order, count=count, access_rights_uid=access_rights_uid)
    #     except ValueError:
    #         raise AccessError(_('You do not have access to this document.'))
    #     if not count and isinstance(ids, Query):
    #         # the result is expected from this table, so we should link tables
    #         ids = super(HrEmployeePrivate, self.sudo())._search([('id', 'in', ids)])
    #     return ids
