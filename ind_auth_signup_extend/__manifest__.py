# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Auth Signup Extend',
    'version': '1.1',
    'author' : 'Indglobal Digital Private Limited',
    'website': 'https://indglobal.in/',
    'category': 'Signup',
    'summary': 'Inherit Auth Signup',
    'description': """
This module extend the features of Login Page.
    """,
    'depends': ['base', 'auth_signup', 'web'],
    'data': [
        'views/auth_signup_login_templates_extend.xml',
    ],
    'installable': True,
    'auto_install': False
}
