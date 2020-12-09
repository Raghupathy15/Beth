# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'CRM Extend',
    'version': '1.1',
    'author' : 'Indglobal Digital Private Limited',
    'website': 'https://indglobal.in/',
    'category': 'crm',
    'summary': 'Inherit Crm',
    'description': """
This module extend the features of CRM.
    """,
    'depends': ['base', 'crm', 'sale', 'sale_crm', 'l10n_in', 'ind_access_extend'],
    'data': [
        'security/groups.xml', 'security/ir.model.access.csv',
        'views/crm_extend_views.xml',
        'data/crm_data.xml'
    ],
    'installable': True,
    'auto_install': False
}
