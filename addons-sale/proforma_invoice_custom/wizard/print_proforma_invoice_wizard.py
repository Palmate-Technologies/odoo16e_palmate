# -*- coding: utf-8 -*-

from odoo import models, fields


class PrintProformaWizard(models.TransientModel):
    _name = 'print.proforma.wizard'
    _description = 'Print Proforma Invoice.Wizard'

    description = fields.Text(string='Description', required=True)
    amount = fields.Float(string="Amount", required=True)
    qty = fields.Float(string="Quantity", default=1)


    def print_proforma_custom(self):
        self.ensure_one()
        ctx = dict(self._context)
        # ctx['desc'] = self.description
        # ctx['amount'] = self.amount
        # self= self.with_context(ctx)
        order = self.env['sale.order'].with_context(ctx).browse(self._context.get('active_id',False))
        data = {
            'model': 'print.proforma.wizard',
            'ids':self._context.get('active_id',False),
            # 'form': order.read()[0],
            'description': self.description,
            'amount': self.amount,
            'quantity': self.qty,
            'payment_term': order.payment_term_id.name,
            'name': order.name,
            'partner': order.partner_id.name,
            'currency_symbol': order.currency_id.symbol,
            'partner_address': order.partner_id.street,
            'partner_vat': order.partner_id.vat,
            'partner_zip': order.partner_id.zip,
            'partner_city': order.partner_id.city,
            'partner_country': order.partner_id.country_id.name,
            'notes': order.note,
            'customer_ref': order.client_order_ref,
            'order_date': order.date_order,
            'validity_date': order.validity_date,
            'salesperson': order.user_id.name,
        }
        # data = {
        #     'ids': [],
        #     'model': 'sale.order',
        #     'form': ctx,
        # }
        return self.env.ref('proforma_invoice_custom.proforma_invoice_report_custom').with_context(ctx).report_action(order, data=data)