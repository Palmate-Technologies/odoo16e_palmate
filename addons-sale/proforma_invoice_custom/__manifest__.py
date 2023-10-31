# -*- coding: utf-8 -*-
{
    'name': "Proforma Invoice Custom",

    'summary': """
        -Proforma Invoice Customization.
    """,
    'description': """
        -Proforma Invoice Customization.
""",
    'author': "Palmate",
    'website': "www.palmate.sa",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sale',
    'version': '16.0.0.1',
    'license': 'AGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale','sales_team'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'wizard/print_proforma_invoice_wizard.xml',
        'report/report.xml',
        'report/proforma_invoice_custom.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
