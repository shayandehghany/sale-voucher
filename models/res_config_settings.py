from odoo import models, fields

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    credit_alert_active = fields.Boolean(
        string='Automatic due date alert enabled',
        config_parameter='sale_voucher.credit_alert_active'
    )
    credit_alert_days_before = fields.Integer(
        string='Number of warning days before due (general)',
        config_parameter='sale_voucher.credit_alert_days_before'
    )
    credit_alert_user_id = fields.Many2one(
        'res.users',
        string='User receiving the alert',
        config_parameter='sale_voucher.credit_alert_user_id'
    )
