# -*- coding: utf-8 -*-
{
    'name': 'QZHub diciplinary tracking',
    'summary': """
        QZHub Attendance""",

    'description': """
        QZHub Attendance
    """,
    'license': "AGPL-3",

    'author': "Qzhub",
    'website': "https://ppm.qzhub.com/web",

    'category': 'Generic Modules/Human Resources',
    'version': '0.1',
    'depends': ['base', 'hr', 'hr_disciplinary_tracking'],
    'data': [
             'views/disciplinary_action.xml',
    ],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
