# -*- coding: utf-8 -*-
from datetime import datetime, date, timedelta
from odoo import models, fields, api, _
from odoo.exceptions import Warning


class HrEmployeeDocument(models.Model):
    _inherit = 'hr.employee.document'

    state = fields.Selection([('draft', 'Draft'),
                              ('to_approve', 'Waiting For Approval'),
                              ('approved', 'Approved'),
                              ('rejected', 'Rejected'),
                              ('expired', 'Expired')], string='Status', default='draft',
                             track_visibility='always', group_expand='_expand_states')

    def _expand_states(self, states, domain, order):
        return [key for key, val in type(self).state.selection]

    rejected_reason = fields.Text(string='Rejected Reason', copy=False, readonly=1, help="Reason for the rejection")

    def sent(self):
        self.state = 'to_approve'

    def approve(self):
        self.state = 'approved'
        if self.document_name.document_type == 'entry':
            self.employee_ref.write({'entry_checklist': [(4, self.document_name.id)]})
        if self.document_name.document_type == 'exit':
            self.employee_ref.write({'exit_checklist': [(4, self.document_name.id)]})

    def set_to_draft(self):
        self.state = 'draft'

    @api.model
    def check_for_date_expiry(self):
        self.search([('state', '=', 'approved'),
                     ('expiry_date', '<=', fields.Date.to_string(date.today())), ]).write({'state': 'expired'})
