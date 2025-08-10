from odoo import models, fields, api,_

class SaleVoucher(models.Model):
    _name = 'sale.voucher'
    _description = 'Sale Voucher'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='voucher id', default='New', readonly=True, copy=False)
    partner_id = fields.Many2one('res.partner', string='partner', required=True, readonly=True, states={'draft': [('readonly', False)]})
    date = fields.Date(string='date', default=fields.Date.context_today, readonly=True, states={'draft': [('readonly', False)]})
    sale_order_id = fields.Many2one('sale.order', string='sale order', required=True, readonly=True)
    voucher_line_ids = fields.One2many('sale.voucher.line', 'voucher_id', string='products', readonly=True, states={'draft': [('readonly', False)]})
    state = fields.Selection([
        ('draft', 'draft'),
        ('account_approved', 'account_approved'),
        ('done', 'done')
    ], string='state', default='draft', tracking=True)

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('sale.voucher') or _('New')
        return super(SaleVoucher, self).create(vals)

    def action_approve_account(self):
        self.write({'state': 'account_approved'})

    def action_done(self):
        self.write({'state': 'done'})




class SaleVoucherLine(models.Model):
    _name = 'sale.voucher.line'
    _description = 'sale voucher line or items'

    voucher_id = fields.Many2one('sale.voucher', string='sale voucher', ondelete='cascade')
    product_id = fields.Many2one('product.product', string='product', required=True)
    quantity = fields.Float(string='amount', required=True, default=1.0)