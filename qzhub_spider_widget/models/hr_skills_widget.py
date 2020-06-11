from odoo.exceptions import Warning
from odoo import models, fields, api, _


class Employee(models.Model):
    _inherit = 'hr.employee'

    spider_widget = fields.Char('Spider Widget',
                                help='Display spider chart in form view')


class EmployeeSkill(models.Model):
    _inherit = 'hr.employee.skill'

    @api.model
    def gotSkills(self, employee_id):
        skills = self.search([['employee_id', '=', employee_id]])
        data = []
        for skill in skills:
            data.append({
                'label': skill.skill_id.name,
                'level': skill.skill_level_id.level_progress
            })

        return data