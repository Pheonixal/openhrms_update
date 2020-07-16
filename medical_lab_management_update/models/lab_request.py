import datetime
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class LabRequest(models.Model):
    _name = 'lab.request'

    def set_to_test_completed(self):
        if not self.request_line:
            raise ValidationError(_("No Result Lines Entered !"))
        req_obj = self.env['lab.request'].search_count([('app_id', '=', self.app_id.id),
                                                        ('id', '!=', self.id)])
        req_obj_count = self.env['lab.request'].search_count([('app_id', '=', self.app_id.id),
                                                              ('id', '!=', self.id),
                                                              ('state', '=', 'completed')])
        if req_obj == req_obj_count:
            app_obj = self.env['lab.appointment'].search([('id', '=', self.app_id.id)])
            app_obj.write({'state': 'completed'})
        for attribute in self.request_line:
            print("Result", attribute.result)
            print("Internal", attribute.interval)
        print("self", self)
        print("Request line", self.request_line)
        return self.write({'state': 'completed'})