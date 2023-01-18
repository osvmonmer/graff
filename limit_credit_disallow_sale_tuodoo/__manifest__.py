# -*- coding: utf-8 -*-
{
    'name': "limit_credit_disallow_sale_tuodoo",

    'summary': """ """,

    'description': """
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",
    'category': 'Uncategorized',
    'version': '14.0.0.1',
    'depends': ['sale','account'],
    'data': [
        # 'security/ir.model.access.csv',
        'security/limit_security.xml',
        'views/sale_order_views.xml',
        'views/stock_picking_views.xml',
        'views/res_partner_views.xml',
        'views/account_payment_term_views.xml',
    ],
}
