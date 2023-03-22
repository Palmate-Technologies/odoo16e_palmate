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

try:
    from num2words import num2words
except ImportError:
    logging.getLogger(__name__).warning("The num2words python library is not installed, Amount in Arabic features won't be fully available.")
    num2words = None


class AccountMove(models.Model):
    _inherit = 'account.move'

    def get_total_discount(self):
        disc_amount = 0
        for line in self.invoice_line_ids:
            if line.discount:
                disc_amount += (line.quantity * line.price_unit) * (line.discount / 100)

        return disc_amount

    # def get_amount_ar(self, amount=0.0):
    #     if num2words is None:
    #         logging.getLogger(__name__).warning("The library 'num2words' is missing, cannot render textual amounts.")
    #         return ""
    #     try:
    #         return self.currency_id.with_context(lang='ar_001').get_amount_text_in_arabic(amount)
    #     except NotImplementedError:
    #         return self.currency_id.with_context(lang='en_US').get_amount_text_in_arabic(amount)