from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'


    credit_limit = fields.Float(string="Credit Limit", required=True)
    credit_due_days = fields.Integer(string="Credit Due Days", required=True ,)
    credit_warn_days = fields.Integer(string="Credit Warn Days", required=True)


    # open_credit_debit = fields.Monetary(
    #     string="Open Credit Debit",
    #     compute='_compute_total_open_credit_amount',
    #
    # )
    #
    # def _compute_total_open_credit_amount(self):
    #     credit_transaction = self.env['credit.transaction']
    #     for partner in self:
    #         total_open_credit = credit_transaction.search([
    #             ('state', '=', 'draft'),
    #             ('partner_id', '=', partner.id)
    #         ])
    #         partner.open_credit_debit = sum(total_open_credit.mapped('amount'))
    #
