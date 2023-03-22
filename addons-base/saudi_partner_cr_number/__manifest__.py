# -*- coding: utf-8 -*-

{
    'name': 'Customer/Vendor CR Number',
    'version': '1.0.0.1',
    'summary': """New field CR Number in the Partner Form""",
    'description': """New field CR Number in the Partner Form""",
    'category': 'Base',
    'author': 'Palmate',
    'license': 'AGPL-3',

    'price': 0.0,
    'currency': 'USD',

    'depends': ['base'],

    'data': [
        'views/res_partner.xml',
        'views/res_company.xml',

    ],
    'demo': [

    ],
    'images': ['static/description/banner.png'],
    'qweb': [],

    'installable': True,
    'auto_install': False,
    'application': False,
}
