# -*- coding: utf-8 -*-
{
    'name': "QZHub document",

    'summary': """
        QZHub document""",

    'description': """
        QZHub document
    """,

    'author': "Qzhub",
    'website': "https://qzhub.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr', 'oh_employee_documents_expiry'],

    # always loaded
    'data': [
        'report/document_report.xml',
        'report/document_templates.xml',
        'views/hr_document_template.xml',
    ],
}
