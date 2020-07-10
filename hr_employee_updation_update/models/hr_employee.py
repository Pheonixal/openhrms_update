# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from odoo import models, fields, _, api
from datetime import date

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    address_home_id = fields.Many2one(
        'res.partner', 'Contact',
        groups="hr.group_hr_user", tracking=True,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    private_email = fields.Char(related='address_home_id.email', string="Private Email", groups="hr.group_hr_user")

    home_address = fields.Char(related='address_home_id.email', string="Address")
    # additional fields
    bank_name = fields.Char(string="Name of the bank")
    iic = fields.Char(string="Individual identification code")
    bic = fields.Char(string="Bank identification code")
    iban = fields.Char(string="IBAN")
    nationality = fields.Char(string="Nationality")

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
    age_from_born = fields.Char(compute='_get_age_from_born_date')

    def _get_age_from_born_date(self,):
        if self.birthday:
            my_str = str(self.birthday).split("-")
            born = date(int(my_str[0]), int(my_str[1]), int(my_str[2]))
            today = date.today()
            self.age_from_born = str(today.year - born.year - ((today.month, today.day) < (born.month, born.day)))
        else:
            self.age_from_born = ""


class EmployeeRelationInfo(models.Model):
    """Table for keep employee family information"""

    _inherit = 'hr.employee.relation'

    name = fields.Char(string="Relationship", help="Relationship with the employee")
