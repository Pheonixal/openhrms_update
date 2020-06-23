from odoo import api, fields, models, _
from odoo.osv import expression

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    def _compute_employee_courses(self):
        res_user_id = self.env['res.users'].search([('id', '=', self.user_id.id)])
        slide_channels = self.env['slide.channel.partner'].search([('partner_id', '=', res_user_id.partner_id.id), ('completed', '=',False)])

        self.course_count = len(slide_channels)

    course_count = fields.Integer(string="Course Count", compute='_compute_employee_courses')

    def get_slide_channels(self):
        action = self.env.ref('website_slides_update.slide_channel_course').read()[0]
        channel_ids_in = []

        res_user_id = self.env['res.users'].search([('id', '=', self.user_id.id)])
        # print(res_user_id)
        slide_channels = self.env['slide.channel.partner'].search([('partner_id','=',res_user_id.partner_id.id), ('completed', '=',False)])
        # print(slide_channels)

        for i in slide_channels:
            channel_ids_in.append(i.channel_id.id)
        # print(channel_ids_in)

        action['domain'] = [('id', '=', channel_ids_in)]
        # print(self.id)

        return action
