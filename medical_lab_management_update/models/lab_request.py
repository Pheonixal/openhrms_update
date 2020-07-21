import datetime
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class LabRequest(models.Model):
    _inherit = 'lab.request'

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

        permiss = []  # Creating new list to save values of operations
        note = ""  # New variable to save results of checks
        for attribute in self.request_line:
            if attribute.result:
                if attribute.interval and attribute.interval_max:
                    check = attribute.interval < attribute.result < attribute.interval_max
                    if not check:
                        note += f"Content :'{attribute.test_content.content_type_name}' result:'{attribute.result} {attribute.unit.unit}' is not between referred intervals of from '{attribute.interval}' to '{attribute.interval_max} {attribute.unit.unit}'\n"
                    permiss.append(check)
                elif attribute.interval:
                    check = attribute.interval < attribute.result
                    if not check:
                        note += f"Content: '{attribute.test_content.content_type_name}' result:'{attribute.result} {attribute.unit.unit}' is less than referred min value of '{attribute.interval} {attribute.unit.unit}'\n"
                    permiss.append(check)
                elif attribute.interval_max:
                    check = attribute.result < attribute.interval_max
                    if not check:
                        note += f"Content {attribute.test_content.content_type_name} result:'{attribute.result} {attribute.unit.unit}' is more than referred max value of '{attribute.interval_max} {attribute.unit.unit}'\n"
                    permiss.append(check)
        self.app_id.comment = note
        if all(permiss):
            self.app_id.permission = 'granted'
        else:
            self.app_id.permission = 'denied'
        return self.write({'state': 'completed'})
