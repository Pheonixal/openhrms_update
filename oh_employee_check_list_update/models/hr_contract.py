# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class Contract(models.Model):
    _inherit = 'hr.contract'

    @api.model
    def create(self, vals):
        contracts = super(Contract, self).create(vals)
        if not contracts.employee_id.contract_ready:
            raise ValidationError(
                _('You can`t create Contract to user without all sufficient documents!'))
        return contracts
