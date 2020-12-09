# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Sale Extend',
    'version': '1.1',
    'author' : 'Indglobal Digital Private Limited',
    'website': 'https://indglobal.in/',
    'category': 'sale',
    'summary': 'Inherit Crm',
    'description': """
This module extend the features of Sale.
    """,
    'depends': ['base', 'sale', 'sale_stock', 'ind_crm_extend', 'ind_product_extend', 'ind_access_extend', 'sale_product_configurator'],
    'data': [
        'security/groups.xml',
        'views/sale_extend_views.xml',
    ],
    'installable': True,
    'auto_install': False
}
