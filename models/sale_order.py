from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    payment_type = fields.Selection([('cash', 'Cash'), ('credit', 'Credit')], string='Payment Type', default='cash',
                                    required=True)
    credit_transaction_id = fields.Many2one('credit.transaction', string='Credit Transaction', readonly=True,
                                            copy=False)
    due_date = fields.Datetime(string='Due Date', default=fields.Datetime.now)

    def action_confirm(self):
        for order in self:
            if order.payment_type == 'credit':
                credit_transaction = self.env['credit.transaction']
                total_open_credit = credit_transaction.search(
                    [('state', '=', 'draft'), ('partner_id', '=', self.partner_id.id)])
                total_open_credit_amount = sum(total_open_credit.mapped('amount'))
                partner_credit_limit = order.partner_id.credit_limit

                if total_open_credit_amount + order.amount_total >= partner_credit_limit:
                    raise ValidationError(_(
                        f"Customer credit limit ({order.partner_id.credit_limit:,.0f} {order.currency_id.symbol}) is not enough .\n"
                        f"Current Debt: {total_open_credit_amount:,.0f} {order.currency_id.symbol}\n"
                        f"Amount of this order: {order.amount_total:,.0f} {order.currency_id.symbol}\n"
                        f"Total new debt: {total_open_credit_amount + order.amount_total:,.0f} {order.currency_id.symbol}"
                    ))

                order.credit_transaction_id = credit_transaction.create({
                    'partner_id': order.partner_id.id,
                    'sale_order_id': order.id,
                    'amount': order.amount_total,
                    'date': order.date,
                    'state': 'draft',

                })
        return super(SaleOrder, self).action_confirm()

