# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Base Extend',
    'version': '1.1',
    'author' : 'Indglobal Digital Private Limited',
    'website': 'https://indglobal.in/',
    'category': 'base',
    'summary': 'Inherit base',
    'description': """
This module extend the features of Base.
    """,
    'depends': ['base', 'base_setup', 'web', 'ind_access_extend'],
    'data': [
        'views/base_extend_views.xml',
    ],
'qweb': [
        "static/src/xml/menu_extend.xml",
],
    'installable': True,
    'auto_install': False
}