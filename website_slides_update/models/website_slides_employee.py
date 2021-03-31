from odoo import api, fields, models, _
from odoo.osv import expression

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    def _compute_employee_courses(self):
        res_user_id = self.env['res.users'].search([('id', '=', self.user_id.id)])
        slide_channels = self.env['slide.channel.partner'].search([('partner_id', '=', res_user_id.partner_id.id), ('completed', '=',False)])
        slide_channels_instruktash = []
        for i in slide_channels:
            # tags = []
            # for j in i.channel_id.tag_ids:
            #     tags.append(j.name)
            if "instruction" == i.channel_id.category:
                slide_channels_instruktash.append(i)
        self.course_count = len(slide_channels_instruktash)

    course_count = fields.Integer(string="Course Count", compute='_compute_employee_courses')

    def get_slide_channels(self):
        action = self.env.ref('website_slides_update.slide_channel_course').read()[0]
        channel_ids_in = []

        res_user_id = self.env['res.users'].search([('id', '=', self.user_id.id)])
        slide_channels = self.env['slide.channel.partner'].search([('partner_id','=',res_user_id.partner_id.id)])

        for i in slide_channels:
            tags = []
            # for j in i.channel_id.tag_ids:
            #     tags.append(j.name)
            if "instruction" == i.channel_id.category:
                channel_ids_in.append(i.channel_id.id)

        action['domain'] = [('channel_id', '=', channel_ids_in), ('partner_id', '=', res_user_id.partner_id.id)]

        return action


class ChannelUsersRelation(models.Model):
    _inherit = 'slide.channel.partner'

    employee_department = fields.Char(compute="_get_employee_id")
    employee_spec = fields.Char(compute='_get_employee_spec')
    write_date_gen = fields.Char(compute='_get_write_date')

    def _get_write_date(self):
        for record in self:
            if record.create_date != record.write_date:
                record.write_date_gen = record.write_date
            else:
                record.write_date_gen = ""

    def _get_employee_spec(self):
        for record in self:
            user = self.env['res.users'].search([('partner_id', '=', record.partner_id.id)])
            if user.id:
                employee = self.env['hr.employee'].search([('user_id', '=', user.id)])
                record.employee_spec = employee.job_id.name
            else:
                record.employee_spec = ""

    def _get_employee_id(self):
        for record in self:
            user = self.env['res.users'].search([('partner_id', '=', record.partner_id.id)])
            if user.id:
                employee = self.env['hr.employee'].search([('user_id', '=', user.id)])
                record.employee_department = employee.department_id.name
            else:
                record.employee_department = ""


class WebsiteChannelSlide(models.Model):
    _inherit = 'slide.channel'

    category = fields.Selection([
        ('instruction', 'Инструктаж'),
        ('course', 'Курс'),
    ])
    deadline = fields.Date(string='Course deadline')
