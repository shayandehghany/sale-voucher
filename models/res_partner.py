from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'


    credit_limit = fields.Float(string="Credit Limit", required=True)
    credit_due_days = fields.Integer(string="Credit Due Days", required=True ,)
    credit_warn_days = fields.Integer(string="Credit Warn Days", required=True)
