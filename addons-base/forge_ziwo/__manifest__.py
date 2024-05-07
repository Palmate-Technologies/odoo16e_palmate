# -*- coding: utf-8 -*-
{
    'name': 'ZIWO',

    'summary': '''This module integrates Ziwo with Odoo''',

    'description': '''This module integrates Ziwo with Odoo''',

    'author': 'Forge Solutions',
    'website': 'https://www.forge-solutions.com',
    'support': 'info@forge-solutions.com',

    'category': 'Productivity',
    'version': '16.0.6',
    'license': 'Other proprietary',
    
    'depends': ['base', 'bus', 'web', 'crm', 'helpdesk', 'sale', 'sale_subscription', 'project'],

    'installable': True,
    'application': True,
    'proxy_mode': True,
    
    'images': ['static/description/banner.gif'],
    
    'data': [
        'security/ziwo_groups.xml',
        'security/ir.model.access.csv',
        'views/helpdesk_ticket_views_inherit.xml',
        'views/agent_screen_views.xml',
        'views/crm_lead_views_inherit.xml',
        'views/sale_order_views_inherit.xml',
        'views/project_task_views_inherit.xml',
        'views/res_partner_views_inherit.xml',
        'views/ziwo_active_form_views.xml',
        'views/res_config_settings_views_inherit.xml',
        'views/ziwo_history_views.xml',
        'wizards/add_note_wizard_views.xml',
        'wizards/edit_contact_wizard_views.xml',
        'wizards/create_call_wizard_views.xml',
        'static/src/xml/ziwo_web_component.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'forge_ziwo/static/src/xml/dialing_panel.xml',
            'forge_ziwo/static/src/scss/ziwo.scss',
            'forge_ziwo/static/src/js/agent_screen_detector.js',
            'forge_ziwo/static/src/js/dialing_panel.js',
            'forge_ziwo/static/src/js/ziwo_dialing_adapter.js',
            'forge_ziwo/static/src/js/dialing_panel_container.js',
            'forge_ziwo/static/src/js/ziwo_systray_item.js',
            'forge_ziwo/static/src/js/ziwo_service.js',
            'forge_ziwo/static/src/js/main.js',
        ],
    },

    'demo': [
    ],
}
