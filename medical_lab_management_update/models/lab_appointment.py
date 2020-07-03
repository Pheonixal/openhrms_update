import datetime
from odoo.exceptions import UserError
from odoo import fields, models, api, _


class Appointment(models.Model):
    _inherit = 'lab.appointment'

    type_of_appointment = fields.Selection(
        [('daily', 'Daily'),
         ('monthly', 'Monthly'),
         ('quarter', 'Quarter')
         ]
    )
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirmed'),
        ('request_lab', 'Lab Requested'),
        ('completed', 'Test Result'),
        ('cancel', 'Cancelled'),
    ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='draft',
    )