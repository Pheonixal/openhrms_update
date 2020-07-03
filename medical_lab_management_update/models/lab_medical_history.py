import datetime
from odoo.exceptions import UserError
from odoo import fields, models, api, _


class MedicalHistory(models.Model):
    _name = 'lab.medical.history'

    name = fields.Char(string="Underlying disease", help="Name of current disease or ailment")

    supervision_start = fields.Date(string="Beginning of Supervision")
    supervision_end = fields.Date(string="End of Supervision")