# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.osv import expression


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    appointments_count = fields.Char(string="Appointments")

    # Medical information of employee
    rhesus_factor = fields.Selection([
        ('rh_plus', 'Rh+'),
        ('rh_minus', 'Rh-')
    ], string="Rhesus factor")
    allergy = fields.Char(string="Allergic reactions")
    phys_condition = fields.Char(string="Physiological condition", help="Physiological condition of the patient")
    pathologies = fields.Char(strong="Hereditary pathologies")
    bad_habits = fields.Char(sring="Bad habits")
    blood_group = fields.Selection(
        [('A+', 'A+ve'), ('B+', 'B+ve'), ('O+', 'O+ve'), ('AB+', 'AB+ve'),
         ('A-', 'A-ve'), ('B-', 'B-ve'), ('O-', 'O-ve'), ('AB-', 'AB-ve')],
        'Blood Group')


    def patient_view(self):
        for each1 in self:
            res_user_id = self.env['res.users'].search([('id', '=', each1.user_id.id)])
            lab_patient = self.env['lab.patient'].search([('patient', '=', res_user_id.partner_id.id)])

            lab_ids = []
            for each in lab_patient:
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


