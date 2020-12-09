{
    'name' : 'Holiday Master',
    'version' : '1.1',
	'author' : 'Indglobal digital private limited',
    'summary': ' Holiday Master',
    'sequence': 1,
    'description': """Adding new master""",
    'category' : 'base',
    'website': 'https://www.indglobal.com',
    'depends' : ['base','contacts'],
    'data': [
            'security/ir.model.access.csv',
            'views/holiday_master_views.xml',
            ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'OEEL-1',
}