# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.osv import expression


class LabPatient(models.Model):
    _inherit = 'lab.patient'

    # Personal information get from hr.employee of connected res.partner
    company_id = fields.Many2one('res.company', string='Company', compute="_compute_info")
    department_id = fields.Many2one('hr.department', string='Department', domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    job_id = fields.Many2one('hr.job', string='Job Position', domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    address_id = fields.Many2one('res.partner', string='Work Address', domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    iin = fields.Char(string='IIN')
    nationality = fields.Char(string='Nationality')
    country_id = fields.Many2one('res.country', 'Customer Country', readonly=True)
    address_home_id = fields.Many2one(
        'res.partner', 'Address', help='Enter here the private address of the employee, not the one linked to your company.',
        groups="hr.group_hr_user", tracking=True,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    marital = fields.Selection([
        ('single', 'Single'),
        ('married', 'Married'),
        ('cohabitant', 'Legal Cohabitant'),
        ('widower', 'Widower'),
        ('divorced', 'Divorced')
    ], string='Marital Status', groups="hr.group_hr_user", default='single', tracking=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], groups="hr.group_hr_user", default="male", tracking=True)

    phone = fields.Char(string="Phone", required=False)

    # Medical information of employee
    rhesus_factor = fields.Selection([
        ('rh_plus', 'Rh+'),
        ('rh_minus', 'Rh-')
    ], string="Rhesus factor")
    allergy = fields.Char(string="Allergic reactions")
    phys_condition = fields.Char(string="Physiological condition", help="Physiological condition of the patient")
    pathologies = fields.Char(strong="Hereditary pathologies")
    bad_habits = fields.Char(sring="Bad habits")

    @api.depends("patient")
    def _compute_info(self):
        for pat in self:
            res_user_id = self.env['res.users'].search([('partner_id', '=', pat.patient.id)])
            emp = self.env['hr.employee'].search([('user_id', '=', res_user_id.id)])
            if emp:
                if emp.company_id:
                    pat.company_id = emp.company_id
                if emp.department_id:
                    pat.department_id = emp.department_id.id
                if emp.job_id:
                    pat.job_id = emp.job_id.id
                if emp.address_id:
                    pat.address_id = emp.address_id.id
                if emp.image_1920:
                    pat.patient_image = emp.image_1920
                if emp.iin:
                    pat.iin = emp.iin
                if emp.nationality:
                    pat.nationality = emp.nationality
                if emp.country_id:
                    pat.country_id = emp.country_id.id
                if emp.address_home_id:
                    pat.address_home_id = emp.address_home_id
                if emp.marital:
                    pat.marital = emp.marital
                if emp.birthday:
                    pat.dob = emp.birthday
                if emp.gender:
                    pat.gender = emp.gender
                if emp.work_phone:
                    pat.phone = emp.work_phone
