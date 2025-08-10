# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'sale voucher',
    'version': '1.0',
    'summary': 'create a sale voucher factor',
    'sequence': 0,
    'description': '''sale voucher management''',
    'category': 'Productivity',
    'website': 'https://www.odoo.com/page/billing',
    'license': 'LGPL-3',
    'depends': ['base',
                'mail',
                'contacts',
                'sale',
                ],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'data/cron_data.xml',
        'views/res_partner_view.xml',
        'views/sale_order_view.xml',
        'views/credit_transaction_view.xml',
        'views/res_config_settings_view.xml',
        'views/sale_voucher_view.xml',
        'report/sale_voucher_report.xml',
        'report/sale_voucher_template.xml'
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,

}
