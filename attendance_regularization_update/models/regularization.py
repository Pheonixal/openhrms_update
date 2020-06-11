from odoo import fields, api, models


class Regular(models.Model):
    _inherit = 'attendance.regular'

    reg_category = fields.Many2one(comodel_name='reg.categories',
                                   string='Regularization Category',
                                   help='Choose the category of attendance regularization',
                                   required=True,
                                   translate=True)