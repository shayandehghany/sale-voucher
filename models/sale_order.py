from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import timedelta, date


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    payment_type = fields.Selection([('cash', 'Cash'), ('credit', 'Credit')], string='Payment Type', default='cash',
                                    required=True)
    credit_transaction_id = fields.Many2one('credit.transaction', string='Credit Transaction', readonly=True,
                                            copy=False)
    due_date = fields.Datetime(string='Due Date', default=fields.Datetime.now)
    voucher_id = fields.Many2one('sale.voucher', string='sale voucher', readonly=True, copy=False)

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
                    'state': 'draft',

                })
        return super(SaleOrder, self).action_confirm()

    def action_mark_as_paid(self):
        for order in self:
            order.credit_transaction_id.write({'state': 'posted'})

    def create_sale_voucher(self):
        self.ensure_one()
        voucher_lines = []
        for line in self.order_line.filtered(lambda l: not l.display_type):
            voucher_lines.append((0, 0, {
                'product_id': line.product_id.id,
                'quantity': line.product_uom_qty,
            }))

        voucher = self.env['sale.voucher'].create({
            'partner_id': self.partner_id.id,
            'sale_order_id': self.id,
            'voucher_line_ids': voucher_lines,
        })

        self.write({'voucher_id': voucher.id})

        return self.action_view_voucher()

    def action_view_voucher(self):
        self.ensure_one()
        return {
            'name': 'sale voucher',
            'type': 'ir.actions.act_window',
            'res_model': 'sale.voucher',
            'res_id': self.voucher_id.id,
            'view_mode': 'form',
            'target': 'current',
        }


@api.model


def _run_credit_due_date_check_alternative(self):
    config = self.env['ir.config_parameter'].sudo()
    if not config.get_param('sale_voucher.credit_alert_active'):
        return

    default_warn_days = int(config.get_param('sale_voucher.credit_alert_days_before', 0))
    user_id = config.get_param('sale_voucher.credit_alert_user_id')

    if not user_id:
        return

    user_id = int(user_id)
    today = date.today()

    orders = self.search([('payment_type', '=', 'credit'), ('state', 'in', ['sale', 'sent'])])

    for order in orders:
        partner = order.partner_id
        warn_days = partner.credit_warn_days or default_warn_days

        warning_date = order.due_date - timedelta(days=warn_days)

        if today == warning_date:
            message = (
                f"Due date alert for Sale Order: <a href='#' data-oe-model='sale.order' data-oe-id='{order.id}'>{order.name}</a> "
                f"for partner '{partner.name}' in the amount {order.amount_total} {order.currency_id.symbol} "
                f"in date {order.due_date} It is due."
            )

            self.env['mail.activity'].create({
                'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
                'summary': 'Payment due warning (from Sale Order)',
                'note': message,
                'res_id': order.id,
                'res_model_id': self.env.ref('sale.model_sale_order').id,
                'user_id': user_id,
            })
