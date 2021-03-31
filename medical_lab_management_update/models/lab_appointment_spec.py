import datetime
from odoo.exceptions import UserError, ValidationError
from odoo import fields, models, api, _


class AppointmentSpec(models.Model):
    _name = 'lab.appointment.specification'

    name = fields.Char()
    physician_id = fields.Many2one('res.partner', string='Referred By', select=True)

    daily_app_time_from = fields.Float(string="Daily Appointment start time")
    daily_app_time_to = fields.Float(string="Daily Appointment end time")

    def appointment_spec(self):
        app_spec_obj = self.env['lab.appointment.specification'].search([])
        app_ids = []
        for each in app_spec_obj:
            app_ids.append(each.id)
        view_id = self.env.ref('medical_lab_management_update.lab_medical_specification_form_view').id
        if app_ids:
            value = {
                'view_mode': 'form',
                'res_model': 'lab.appointment.specification',
                'view_id': view_id,
                'type': 'ir.actions.act_window',
                'name': _('Appointment Daily'),
                'res_id': app_ids and app_ids[0]
            }
            return value
