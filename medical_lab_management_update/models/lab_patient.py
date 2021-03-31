# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.osv import expression
from dateutil.relativedelta import relativedelta
import logging
import datetime
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
    gender = fields.Char(strring="Gender", compute="_compute_detail")

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

    height = fields.Char(string="Height")
    weight = fields.Char(string="Weight")

    def _compute_history_count(self):
        for obj in self:
            obj.medical_history_count = self.env['lab.medical.history'].search_count([('patient', '=', obj.patient.id)])

    def _compute_state(self):
        for obj in self:
            obj.app_count = self.env['lab.appointment'].search_count([('patient_id', '=', obj.id), ('state', 'not in', ('cancel', 'invoiced'))])

    def compute_age(self):
        for data in self:
            data.age = ''
            if data.dob:
                dob = fields.Datetime.from_string(data.dob)
                date = fields.Datetime.from_string(data.date)
                delta = relativedelta(date, dob)
                data.age = str(delta.years)

    @api.depends('patient')
    def _compute_detail(self):
        """ Function to get info from employee
        """
        for rec in self:
            rec.gender = ''
            rec.phone = rec.patient.phone
            rec.email = rec.patient.work_email
            rec.company_id = rec.patient.company_id.id
            rec.department_id = rec.patient.department_id.id
            rec.job_id = rec.patient.job_id.id
            rec.address_id = rec.patient.address_id.id
            rec.nationality = rec.patient.nationality
            rec.country_id = rec.patient.country_id.id
            rec.address_home_id = rec.patient.address_home_id.id
            rec.marital = rec.patient.marital
            rec.dob = rec.patient.birthday
            if rec.patient.gender:
                rec.gender = rec.patient.gender.capitalize()
            rec.phone = rec.patient.work_phone

    @api.onchange('patient')
    def detail_get(self):
        """ Function to get image from employee
        """
        self.patient_image = self.patient.image_1920
