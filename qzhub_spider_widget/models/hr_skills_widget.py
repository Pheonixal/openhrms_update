from odoo.exceptions import Warning
from odoo import models, fields, api, _


class Employee(models.Model):
    _inherit = 'hr.employee'

    spider_widget = fields.Char('Spider Widget',
                                help='Display spider chart in form view', default = "spiderwidget")

class EmployeePublic(models.Model):
    _inherit = 'hr.employee.public'

    spider_widget = fields.Char('Spider Widget',
                                help='Display spider chart in form view', default="spiderwidget")



class EmployeeSkill(models.Model):
    _inherit = 'hr.employee.skill'
    required_level_progress = fields.Integer(related='skill_level_id.required_level_progress')

    @api.model
    def gotSkills(self, employee_id):
        skills = self.search([['employee_id', '=', employee_id]])
        data = []
        for skill in skills:
            data.append({
                'label': skill.skill_id.name,
                'level': skill.skill_level_id.level_progress,
                'required_level': skill.skill_level_id.required_level_progress,
                'label_id': skill.id,
            })

        return data

class SkillLevel(models.Model):
    _inherit = 'hr.skill.level'

    required_level_progress = fields.Integer(string="Necessary level", help="Progress from zero knowledge (0%) to fully mastered (100%).")
    level_progress = fields.Integer(string="Current level",
                                    help="Progress from zero knowledge (0%) to fully mastered (100%).")