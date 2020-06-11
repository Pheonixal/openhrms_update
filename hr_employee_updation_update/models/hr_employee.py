# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from odoo import models, fields, _, api


class HrEmployee(models.Model):
    _inherit = 'hr.employee'


    # additional fields
    bank_name = fields.Char(string="Name of the bank")
    iic = fields.Char(string="Individual identification code")
    bic = fields.Char(string="Bank identification code")
    iban = fields.Char(string="IBAN")

    type_of_docs = fields.Selection([
        ('id_card', 'ID card'),
        ('passport', 'Passport'),
    ], string="Document type", groups="hr.group_hr_user", default="id_card")
    iin = fields.Char(string="Individual identification number")
    id_issue_date = fields.Date(string="Issue date", groups="hr.group_hr_user")
    id_given_by = fields.Selection([
        ('mvd', 'Ministry of Internal Affairs of Kazakhstan'),
        ('mj', 'Ministry of Justice of Kazakhstan'),
    ], string="Given by", groups="hr.group_hr_user")


class EmployeeRelationInfo(models.Model):
    """Table for keep employee family information"""

    _inherit = 'hr.employee.relation'

    name = fields.Char(string="Relationship", help="Relationship with the employee")
