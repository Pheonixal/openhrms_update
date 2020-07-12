# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.osv import expression
from dateutil.relativedelta import relativedelta
import logging
_logger = logging.getLogger(__name__)

class LabPatient(models.Model):
    _inherit = 'lab.patient'

    # Personal information get from hr.employee of connected res.partner
    patient = fields.Many2one('hr.employee', string='Patient name', required=True)

    company_id = fields.Many2one('res.company', string='Company')
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
    ], groups="hr.group_hr_user", required=False, tracking=True)

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
    dob = fields.Date(string='Date Of Birth', required=False)

    def _compute_history_count(self):
        for obj in self:
            obj.medical_history_count = self.env['lab.medical.history'].search_count([('patient', '=', obj.patient.id)])

    def compute_age(self):
        for data in self:
            data.age = ''
            if data.dob:
                dob = fields.Datetime.from_string(data.dob)
                date = fields.Datetime.from_string(data.date)
                delta = relativedelta(date, dob)
                data.age = str(delta.years)

    @api.onchange('patient')
    def detail_get(self):
        self.phone = self.patient.phone
        self.email = self.patient.private_email
        self.company_id = self.patient.company_id.id
        self.department_id = self.patient.department_id.id
        self.job_id = self.patient.job_id.id
        self.address_id = self.patient.address_id.id
        self.patient_image = self.patient.image_1920
        self.nationality = self.patient.nationality
        self.country_id = self.patient.country_id.id
        self.address_home_id = self.patient.address_home_id.id
        self.marital = self.patient.marital
        self.dob = self.patient.birthday
        self.gender = self.patient.gender
        self.phone = self.patient.work_phone

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
