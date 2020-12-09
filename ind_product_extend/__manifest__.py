# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Product Extend',
    'version': '1.1',
    'author' : 'Indglobal Digital Private Limited',
    'website': 'https://indglobal.in/',
    'category': 'Product',
    'summary': 'Product Crm',
    'description': """
This module extend the features of Sale.
    """,
    'depends': ['base', 'product', 'account', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_extend_views.xml',
    ],
    'installable': True,
    'auto_install': False
}