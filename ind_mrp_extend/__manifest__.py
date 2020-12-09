# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'MRP Extend',
    'version': '1.1',
    'author' : 'Indglobal Digital Private Limited',
    'website': 'https://indglobal.in/',
    'category': 'Manufacture',
    'summary': 'Inherit mrp',
    'description': """
This module extend the features of Manufacture.
    """,
    'depends': ['base', 'mrp', 'sale', 'ind_sale_extend'],
    'data': ['security/mrp_production_security_extend.xml',
        'security/ir.model.access.csv',
        'views/mrp_extend_views.xml',
        'views/questions_master_view.xml',
        'views/cron.xml',
        'views/capacity_details_view.xml',
    ],
    'installable': True,
    'auto_install': False
}
