# -*- coding: utf-8 -*-
{
    'name': "medical_lab_management_update",

    'summary': """
        Updating medical lab management module""",

    'description': """
        Updating medical lab management module
    """,

    'author': 'Qzhub',
    'company': 'Qzhub',
    'website': "https://www.qzhub.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'medical_lab_management', 'hr', 'hr_employee_updation_update','attendance_regularization'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/hr_employee.xml',
        'views/lab_medical_history.xml',
        'views/lab_patient.xml',
        'views/lab_appointment.xml',
        'views/lab_appointment_spec.xml',
        'views/physician_details.xml',
        'views/lab_request.xml',
        'views/lab_test_type.xml',
        'report/report.xml',
        'report/lab_patient_card.xml',
        'views/examination_cron.xml',
        'data/daily_appointment_spec.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}