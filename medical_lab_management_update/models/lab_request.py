import datetime
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class LabRequest(models.Model):
    _inherit = 'lab.request'
    _order = 'lab_requesting_date desc'

    doc_count = fields.Integer(compute='_compute_attached_docs_count', string="Number of documents attached")

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
                    check = float(attribute.interval) <= float(attribute.result) <= float(attribute.interval_max)
                    if not check:
                        note += f"Content :'{attribute.test_content.content_type_name}' result:'{attribute.result} {attribute.unit.unit}' is not between referred intervals of from '{attribute.interval}' to '{attribute.interval_max} {attribute.unit.unit}'\n"
                    permiss.append(check)
                elif attribute.interval:
                    check = float(attribute.interval) <= float(attribute.result)
                    if not check:
                        note += f"Content: '{attribute.test_content.content_type_name}' result:'{attribute.result} {attribute.unit.unit}' is less than referred min value of '{attribute.interval} {attribute.unit.unit}'\n"
                    permiss.append(check)
                elif attribute.interval_max:
                    check = float(attribute.result) <= float(attribute.interval_max)
                    if not check:
                        note += f"Content {attribute.test_content.content_type_name} result:'{attribute.result} {attribute.unit.unit}' is more than referred max value of '{attribute.interval_max} {attribute.unit.unit}'\n"
                    permiss.append(check)
        self.app_id.comment = note
        if len(permiss) and all(permiss):
            self.app_id.permission = 'granted'
        else:
            self.app_id.permission = 'denied'
        return self.write({'state': 'completed'})


    def _compute_attached_docs_count(self):
        attachment = self.env['ir.attachment']
        for app in self:
            app.doc_count = attachment.search_count([
                '|',
                '&', ('res_model', '=', 'lab.request'), ('res_id', 'in', self.ids),
                '&', ('res_model', '=', 'lab.appointment'), ('res_id', 'in', self.app_id.ids),
            ])

    def attachment_tree_view(self):
        self.ensure_one()
        domain = [
            '|',
            '&', ('res_model', '=', 'lab.request'), ('res_id', 'in', self.ids),
            '&', ('res_model', '=', 'lab.appointment'), ('res_id', 'in', self.app_id.ids),
        ]
        return {
            'name': _('Attachments'),
            'domain': domain,
            'res_model': 'ir.attachment',
            'type': 'ir.actions.act_window',
            'view_id': False,
            'view_mode': 'kanban,tree,form',
            'view_type': 'form',
            'help': _('''<p class="o_view_nocontent_smiling_face">
                                Documents are attached to the tasks and issues of your project.</p><p>
                                Send messages or log internal notes with attachments to link
                                documents to your project.
                            </p>'''),
            'limit': 80,
            'context': "{'default_res_model': '%s','default_res_id': %d}" % (self._name, self.id)
        }
