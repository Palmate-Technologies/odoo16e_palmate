from odoo import models, fields, api, _
from datetime import timedelta
from odoo.exceptions import UserError, ValidationError


class ResPartner(models.Model):
    _inherit = "res.partner"

    ticket_ids = fields.One2many(comodel_name="helpdesk.ticket", inverse_name="partner_id", string="Tickets")
    subscription_ids = fields.One2many(comodel_name="sale.order", inverse_name="partner_id", string="Subscriptions", domain=[('is_subscription', '=', True)])
    task_ids = fields.One2many(comodel_name="project.task", inverse_name="partner_id", string="Tasks")
    calls_ids = fields.One2many(comodel_name="ziwo.history", inverse_name="partner_id", string="Calls")
    mobile = fields.Char(tracking=True)
    
    phone_trim = fields.Char(compute="_trim_number", store=True)
    mobile_trim = fields.Char(compute="_trim_number", store=True)

    #add constrains to make number unique
    @api.constrains('phone_trim', 'mobile_trim')
    def _check_unique_number(self):
        for record in self:
            if record.phone_trim:
                if self.env['res.partner'].sudo().search_count(['|',('mobile_trim', '=', record.phone_trim), ('phone_trim', '=', record.phone_trim), ('active', '=', True)]) > 1:
                    # raise UserError(_("Phone number " + record.phone_trim + " must be unique"))
                    existing_partner = self.env['res.partner'].sudo().search(['|',('mobile_trim', '=', record.phone_trim), ('phone_trim', '=', record.phone_trim), ('active', '=', True), ('id', '!=', record.id)], limit=1)
                    raise UserError(_('Phone number must be unique: already used by "' + existing_partner.name + '" [' + str(existing_partner.id) + ']'))
            if record.mobile_trim:
                if self.env['res.partner'].sudo().search_count(['|',('mobile_trim', '=', record.mobile_trim), ('phone_trim', '=', record.mobile_trim), ('active', '=', True)]) > 1:
                    # raise UserError(_("Mobile number " + record.mobile_trim + " must be unique"))
                    existing_partner = self.env['res.partner'].sudo().search(['|',('mobile_trim', '=', record.mobile_trim), ('phone_trim', '=', record.mobile_trim), ('active', '=', True), ('id', '!=', record.id)], limit=1)
                    raise UserError(_('Mobile number must be unique: already used by "' + existing_partner.name + '" [' + str(existing_partner.id) + ']'))


    @api.depends('phone', 'mobile')
    def _trim_number(self):
        for record in self:
            record["phone_trim"] = record["phone"]
            record["mobile_trim"] = record["mobile"]
            if record["phone"]:
                record["phone_trim"] = record["phone"].replace(' ', '')
            if record["mobile"]:
                record["mobile_trim"] = record["mobile"].replace(' ', '')

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        if name:
            name = name.split(' / ')[-1]
            args = ['|', '|', '|', ('name', operator, name), ('phone_trim', operator, name), ('mobile_trim', operator, name), ('email', operator, name)] + args
        return self._search(args, limit=limit, access_rights_uid=name_get_uid)

    def open_create_call_wizard(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "res_model": "create.call.wizard",
            "view_mode": "form",
            "view_type": "form",
            "target": "new",
            "context": {
                "default_model": 'res.partner',
                "default_record": self.id,
            },
        }
    
    def create_new_call(self):
        self.env['agent.screen'].sudo().create_new_call('res.partner', self.id, self.mobile_trim)
    
    def create_new_call_phone(self):
        self.env['agent.screen'].sudo().create_new_call('res.partner', self.id, self.phone_trim)
