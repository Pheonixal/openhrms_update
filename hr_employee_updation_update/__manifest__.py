# -*- coding: utf-8 -*-
{
    'name': 'QZHub employee upd',
    'version': '13.0.2.0.0',
    'summary': """Adding Advanced Fields In Employee Master""",
    'description': 'This module helps you to add more information in employee records.',
    'category': 'Generic Modules/Human Resources',
    'author': 'Qzhub',
    'company': 'Qzhub',
    'website': "https://www.qzhub.com",
    'depends': ['base', 'hr', 'hr_employee_updation', 'qzhub_spider_widget'],
    'data': [
        'views/hr_employee_view.xml',
        'report/resume_template.xml',
        'report/resume_report.xml',
    ],
    'demo': [],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
    'qweb': ['static/src/xml/hr_templates.xml'],
}
