# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class InheritEmployee(models.Model):
    _inherit = 'hr.employee'

    def _compute_discipline_count(self):
        all_actions = self.env['disciplinary.action'].read_group([
            ('employee_name', 'in', self.ids),
            ('state', '=', 'explain'),
        ], fields=['employee_name'], groupby=['employee_name'])
        mapping = dict([(action['employee_name'][0], action['employee_name_count']) for action in all_actions])
        for employee in self:
            employee.discipline_count = mapping.get(employee.id, 0)

    disciplinary_line_ids = fields.One2many('disciplinary.action', 'employee_name', string="Disciplinary actions")

    just_field = fields.Char(string='Just Field')
    display_type = fields.Selection([('classic', 'Classic')], string="Display Type", default='classic')


class CategoryDiscipline(models.Model):
    _inherit = 'discipline.category'
    _description = 'Reason Category'

    # Discipline Categories

    name = fields.Char(string="Name", required=True, help="Category name", translate=True)


class DisciplinaryAction(models.Model):
    _inherit = 'disciplinary.action'

    date_disciplinary = fields.Date()
    date_action = fields.Date()
    description = fields.Text(string="Description")
    line_type_id = fields.Many2one('hr.resume.line.type', string="Type")
    display_type = fields.Selection([('classic', 'Classic')], string="Display Type", default='classic')
