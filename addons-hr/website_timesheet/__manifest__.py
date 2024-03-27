
{
    'name' : 'website_timesheet',
    'version' : '1.0',
    'summary': '',
    'sequence': 10,
    'description': """ website timesheet for 16 

    """,
    'category': 'Website/Website',
    'depends': ['base','purchase','website','project','hr_timesheet'],
        'data': [
        'views/hr_employee.xml',
       'views/employee_timesheet.xml',
       'views/views.xml',
      'views/project_view.xml',
    ],
   'assets': {
        "web.assets_frontend": [
            "website_timesheet/static/src/*/**",
        ],
    },
   
    'installable': True,
    'application': True,
    'auto_install': False,

}

