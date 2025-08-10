from odoo import models,fields,api,_


class CreditTransaction(models.Model):
    _name = 'credit.transaction'
    _description = 'Credit Transaction'
    _order = 'date desc , id desc'

    partner_id = fields.Many2one('res.partner', string='Partner' , required=True,index=True)
    sale_order_id = fields.Many2one('sale.order', string='Sales Order', readonly=True)
    amount = fields.Monetary(string='amount', related='sale_order_id.amount_total', required=True)
    currency_id = fields.Many2one('res.currency', related='sale_order_id.currency_id', store=True)
    date = fields.Date(string='date', default=fields.Date.context_today, required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('posted', 'posted'),
    ])
    note = fields.Text(string='note')