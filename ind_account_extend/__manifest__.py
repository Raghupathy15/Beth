# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Account Extend',
    'version': '1.1',
    'author' : 'Indglobal Digital Private Limited',
    'website': 'https://indglobal.in/',
    'category': 'account',
    'summary': 'Inherit Crm',
    'description': """
This module extend the features of Account.
    """,
    'depends': ['base', 'account', 'sale', 'ind_sale_extend'],
    'data': ['security/account_security_extend.xml',
        'views/account_extend_views.xml',
    ],
    'installable': True,
    'auto_install': False
}
