# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'User & Access Rights',
    'version': '1.1',
    'author' : 'Indglobal Digital Private Limited',
    'website': 'https://indglobal.in/',
    'category': 'base',
    'summary': 'Access Rights',
    'description': """
This module extend the features of Access rights & Record Rule & customer.
    """,
    'depends': ['base', 'contacts'],
    'data': [
        'security/groups.xml',
        # 'security/ir.model.access.csv',
        # 'views/crm_extend_views.xml',
    ],
    'installable': True,
    'auto_install': False
}