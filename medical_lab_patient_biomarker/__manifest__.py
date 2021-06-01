# -*- coding: utf-8 -*-
{
    'name': "QZHub Patient biomarkers",

    'summary': """
        Qzhub Patient biomarkers""",

    'description': """
        Qzhub Patient biomarkers
    """,

    'author': "TOO QZhub",
    'website': "https://www.qzhub.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Technical Settings',
    'version': '13.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base',
                'medical_lab_management',
                'hr',
                'hr_employee_updation_update',
                'attendance_regularization',
                'medical_lab_management_update'
                ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/lab_patient.xml'
    ],
    'qweb': [
    ],

}
