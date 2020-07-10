# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.osv import expression
import logging
_logger = logging.getLogger(__name__)

class LabPatient(models.Model):
    _inherit = 'lab.patient'

    # Personal information get from hr.employee of connected res.partner
    patient = fields.Many2one('res.partner', string='Patient name', required=True)

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
    preventive_actions = fields.Char(string="Preventive actions", help="Vaccinations")
    chronic_diseases = fields.Char(string="Chronic diseases")
    contraindications = fields.Char(string="Contraindications", help="Specific situation in which a drug, procedure, or surgery should not be used because it may be harmful to the person.")
    operating_pressure = fields.Char(string="Normal blood pressure", help="Blood pressure of employee")

    blood_donor = fields.Boolean(string='Blood donor')
    work_condition = fields.Boolean(string='Hazardous working conditions')

    medical_history_count = fields.Integer(string="Medical History count", compute="_compute_history_count", copy=False, default=0)

    def _compute_history_count(self):
        for obj in self:
            obj.medical_history_count = self.env['lab.medical.history'].search_count([('patient', '=', obj.patient.id)])


    @api.depends("patient")
    def _compute_info(self):
        for pat in self:
            res_user_id = pat.env['res.users'].search([('partner_id', '=', pat.patient.id)])
            print('Res user', res_user_id)
            emp = pat.env['hr.employee'].search([('user_id', '=', res_user_id.id)])
            print('Employee', emp)
            pat.company_id = ''
            if emp:
                empl = emp[0]
                print(empl)
                if empl.company_id:
                    pat.company_id = empl.company_id
                if empl.department_id:
                    pat.department_id = empl.department_id.id
                if empl.job_id:
                    pat.job_id = empl.job_id.id
                if empl.address_id:
                    pat.address_id = empl.address_id.id
                pat.patient_image = empl.image_1920
                if empl.iin:
                    pat.iin = empl.iin
                if empl.nationality:
                    pat.nationality = empl.nationality
                if empl.country_id:
                    pat.country_id = empl.country_id.id
                if empl.address_home_id:
                    pat.address_home_id = empl.address_home_id
                if empl.marital:
                    pat.marital = empl.marital
                if empl.birthday:
                    pat.dob = empl.birthday
                if empl.gender:
                    pat.gender = empl.gender
                if empl.work_phone:
                    pat.phone = empl.work_phone

    @api.model
    def create_medical_examination(self):
        lab_patient = self.env["lab.patient"].search([])
        for pat in lab_patient:
            print(pat)
            print(pat.work_condition)
            if pat.work_condition:
                new = self.env["lab.medical.examination"].sudo().create({
                    'patient': pat.patient.id,
                    'examination_date': fields.Datetime.now(),  # connecting new step to newly created task
                    'type_of_appointment': 'daily',
                })
            print(new)
