from odoo import models, fields, api

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    forge_ziwo_active_form_id = fields.Many2one('ziwo.active.form', string='Default Action')
    forge_ziwo_active_form_history = fields.Boolean(string='History on Active Form')
    forge_ziwo_navigate_outbound_calls = fields.Boolean(string='Navigate (Outbound Calls)')
    forge_ziwo_navigate_outbound_calls_c2c = fields.Boolean(string='Click to Call Override Navigate (Outbound Calls)')
    forge_ziwo_navigate_inbound_calls = fields.Boolean(string='Navigate (Inbound Calls)')
    forge_ziwo_admin_auth_token = fields.Char(string='Admin Auth Token')

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].set_param('forge_ziwo_active_form_id', self.forge_ziwo_active_form_id.id)
        self.env['ir.config_parameter'].set_param('forge_ziwo_active_form_history', self.forge_ziwo_active_form_history)
        self.env['ir.config_parameter'].set_param('forge_ziwo_navigate_outbound_calls', self.forge_ziwo_navigate_outbound_calls)
        self.env['ir.config_parameter'].set_param('forge_ziwo_navigate_outbound_calls_c2c', self.forge_ziwo_navigate_outbound_calls_c2c)
        self.env['ir.config_parameter'].set_param('forge_ziwo_navigate_inbound_calls', self.forge_ziwo_navigate_inbound_calls)
        self.env['ir.config_parameter'].set_param('forge_ziwo_admin_auth_token', self.forge_ziwo_admin_auth_token)

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        params = self.env['ir.config_parameter'].sudo()
        res.update(
            forge_ziwo_active_form_id = int(params.get_param('forge_ziwo_active_form_id')),
            forge_ziwo_active_form_history = params.get_param('forge_ziwo_active_form_history'),
            forge_ziwo_navigate_outbound_calls = params.get_param('forge_ziwo_navigate_outbound_calls'),
            forge_ziwo_navigate_outbound_calls_c2c = params.get_param('forge_ziwo_navigate_outbound_calls_c2c'),
            forge_ziwo_navigate_inbound_calls = params.get_param('forge_ziwo_navigate_inbound_calls'),
            forge_ziwo_admin_auth_token = params.get_param('forge_ziwo_admin_auth_token'),
        )
        return res