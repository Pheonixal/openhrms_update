# -*- coding: utf-8 -*-
{
    'name': "oh_employee_check_list_update",

    'summary': """
        Updating document check list""",

    'description': """
        Updating document check list
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
    'depends': ['base', 'oh_employee_documents_expiry', 'mail', 'hr', 'oh_employee_check_list', 'hr_contract'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        # 'security/security.xml',
        'views/document_expiry_cron.xml',
        'views/wizard_reason_view.xml',
        'views/hr_employee.xml',
        'views/employee_document_view.xml',

    ],
    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/demo.xml',
    # ],
}