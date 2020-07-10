# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.osv import expression
from dateutil.relativedelta import relativedelta
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
    gender = fields.Char(required=False, tracking=True)

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

    @api.depends("patient")
    def _compute_info(self):
        for pat in self:
            res_user_id = pat.env['res.users'].search([('partner_id', '=', pat.patient.id)])
            pat.company_id = ''
            # pat.department_id = ''
            # pat.job_id = ''
            # pat.address_id = ''
            # pat.patient_image = ''
            # pat.iin = ''
            # pat.address_home_id = ''
            # pat.marital = ''
            # pat.dob = ''
            # pat.gender = ''
            # pat.work_phone = ''
            if res_user_id:
                empl = pat.env['hr.employee'].search([('user_id', '=', res_user_id.id)])
                if empl:
                    for emp in empl:
                        if emp:
                            _logger.error('Employee: %s' % str(empl))
                            _logger.error('res_user_id: %s' % str(res_user_id))
                            _logger.error('pat.patient.id: %s' % str(pat.patient.id))
                            # _logger.error('Employee name: %s' % str(emp.name))
                            # _logger.error('company_id: %s' % str(emp.company_id))
                            # _logger.error('department_id: %s' % str(emp.department_id))
                            pat.company_id = emp.company_id.id if emp.company_id else False
                            pat.department_id = emp.department_id.id if emp.department_id else False
                            pat.job_id = emp.job_id.id if emp.job_id else False
                            pat.address_id = emp.address_id.id if emp.address_id else False
                            pat.patient_image = emp.image_1920
                            pat.nationality = emp.nationality
                            pat.country_id = emp.country_id.id if emp.country_id else False
                            pat.address_home_id = emp.address_home_id.id if emp.address_home_id else False
                            pat.address_home_id = emp.address_home_id.id if emp.address_home_id else False
                            pat.marital = emp.marital
                            pat.dob = emp.birthday
                            pat.gender = (emp.gender).capitalize()
                            pat.phone = emp.work_phone

                            # if emp.department_id:
                            #     pat.department_id = emp.department_id.id
                            # if emp.job_id:
                            #     pat.job_id = emp.job_id.id
                            # if emp.address_id:
                            #     pat.address_id = emp.address_id.id
                            # if emp.image_1920:
                            #     pat.patient_image = emp.image_1920
                            # if emp.iin:
                            #     pat.iin = emp.iin
                            # if emp.nationality:
                            #     pat.nationality = emp.nationality
                            # if emp.country_id:
                            #     pat.country_id = emp.country_id.id
                            # if emp.address_home_id:
                            #     pat.address_home_id = emp.address_home_id
                            # if emp.marital:
                            #     pat.marital = emp.marital
                            # if emp.birthday:
                            #     pat.dob = emp.birthday
                            # if emp.gender:
                            #     pat.gender = emp.gender
                            # if emp.work_phone:
                            #     pat.phone = emp.work_phone

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
