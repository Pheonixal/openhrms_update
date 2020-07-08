import datetime
from odoo.exceptions import UserError
from odoo import fields, models, api, _


class Examination(models.Model):
    _name = 'lab.medical.examination'

    name = fields.Char(string="Medical Examination")
    type_of_appointment = fields.Selection(
        [('daily', 'Daily'),
         ('monthly', 'Monthly'),
         ('quarter', 'Quarter')
         ]
    )

    patient = fields.Many2one('res.partner', string='Patient', required=True)
    physician_id = fields.Many2one('res.partner', string='Referred By', select=True)

    examination_date = fields.Datetime(string="Examination date")
    permission = fields.Selection([
        ('granted', 'Granted'),
        ('denied', 'Denied'),
    ], string="Permission", index=True)



    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirmed'),
        ('completed', 'Done'),
        ('cancel', 'Cancelled'),
    ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='draft',
    )

    test_types = fields.One2many('lab.test.type', 'test_types_reverse', string="Test Lines")
    comment = fields.Html(string='Comments')

class LabTestType(models.Model):
    _name = 'lab.test.type'

    name = fields.Char(string="Content of test")
    interval = fields.Char(string="Reference Intervals")
    result = fields.Char(string="Results")
    test_types_reverse = fields.Many2one('lab.medical.examination', string="Request")
