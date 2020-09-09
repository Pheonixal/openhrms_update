# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from datetime import timedelta, datetime, date
from odoo.osv import expression


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    contract_ready = fields.Boolean(default=False, compute='_compute_contract_ready')

    @api.depends('entry_progress')
    def _compute_contract_ready(self):
        for rec in self:
            if rec.entry_progress == 100:
                rec.contract_ready = True
            else:
                rec.contract_ready = False

    def document_view(self):
        self.ensure_one()
        domain = [
            ('employee_ref', '=', self.id)]
        return {
            'name': _('Documents'),
            'domain': domain,
            'res_model': 'hr.employee.document',
            'type': 'ir.actions.act_window',
            'view_id': False,
            'view_mode': 'kanban,tree,form',
            'help': _('''<p class="oe_view_nocontent_create">
                           Click to Create for New Documents
                        </p>'''),
            'limit': 80,
            'context': "{'default_employee_ref': %s}" % self.id
        }