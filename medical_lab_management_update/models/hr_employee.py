# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from datetime import timedelta, datetime, date
from odoo.osv import expression


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    appointments_count = fields.Char(string="Appointments")

    # Medical information of employee
    rhesus_factor = fields.Selection([
        ('rh_plus', 'Rh+'),
        ('rh_minus', 'Rh-')
    ], string="Rhesus factor")
    allergy = fields.Char(string="Allergic reactions", compute="_compute_info")
    phys_condition = fields.Char(string="Physiological condition", help="Physiological condition of the patient")
    pathologies = fields.Char(strong="Hereditary pathologies")
    bad_habits = fields.Char(sring="Bad habits")
    blood_group = fields.Selection(
        [('A+', 'A+ve'), ('B+', 'B+ve'), ('O+', 'O+ve'), ('AB+', 'AB+ve'),
         ('A-', 'A-ve'), ('B-', 'B-ve'), ('O-', 'O-ve'), ('AB-', 'AB-ve')],
        'Blood Group')
    preventive_actions = fields.Char(string="Preventive actions", help="Vaccinations")
    chronic_diseases = fields.Char(string="Chronic diseases")
    contraindications = fields.Char(string="Contraindications",
                                    help="Specific situation in which a drug, procedure, or surgery should not be used because it may be harmful to the person.")
    operating_pressure = fields.Char(string="Normal blood pressure", help="Blood pressure of employee")
    blood_donor = fields.Boolean(string='Blood donor')
    work_condition = fields.Boolean(string='Hazardous working conditions')
    is_patient = fields.Boolean(string='Is Patient')
    patient_id = fields.One2many('lab.patient', 'patient', string="Lab Patient")

    def patient_view(self):
        for each1 in self:
            # res_user_id = self.env['res.users'].search([('id', '=', each1.user_id.id)])
            # lab_patient = self.env['lab.patient'].search([('patient', '=', res_user_id.partner_id.id)])

            lab_ids = []
            for each in each1:
                lab_ids.append(each.id)
            view_id = self.env.ref('medical_lab_management.view_lab_patient_form').id
            if lab_ids:
                value = {
                    'view_mode': 'form',
                    'res_model': 'lab.patient',
                    'view_id': view_id,
                    'type': 'ir.actions.act_window',
                    'name': _('Custody'),
                    'res_id': lab_ids and lab_ids[0]
                }

                return value

    @api.depends('address_home_id')
    def _compute_info(self):
        """ Function to get info from medical card to employee passprort
        :return:
        :rtype:
        """
        for emp in self:
            patient = self.env['lab.patient'].search([('patient', '=', emp.id)])
            emp.allergy = ''
            if patient:
                emp.bad_habits = patient.bad_habits
                emp.blood_group = patient.blood_group
                emp.blood_donor = patient.blood_donor
                emp.work_condition = patient.work_condition
                emp.allergy = patient.allergy
                emp.rhesus_factor = patient.rhesus_factor
                emp.phys_condition = patient.phys_condition
                emp.pathologies = patient.pathologies
                emp.preventive_actions = patient.preventive_actions
                emp.chronic_diseases = patient.chronic_diseases
                emp.contraindications = patient.contraindications
                emp.operating_pressure = patient.operating_pressure

    # @api.model
    # def get_dept_employee(self):
    #     examination = self.env['lab.medical.examination'].search([])
    #     data = []
    #     for exam in examination:
    #         if exam.examination_date and exam.examination_date.date() == datetime.now().date():
    #             data.append({
    #                 'label': exam.patient.name,
    #                 'value': exam.permission.capitalize() if exam.permission else 'TBA'
    #             })
    #     return data






