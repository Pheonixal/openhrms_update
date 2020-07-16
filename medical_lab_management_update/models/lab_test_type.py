from odoo import models, fields


class LabTestAttribute(models.Model):
    _inherit = 'lab.test.attribute'

    # unit = fields.Many2one('uom.uom', string="Unit")
    interval = fields.Char(string="Min Value")
    interval_max = fields.Char(string="Max Value")
