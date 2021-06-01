# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
import logging
_logger = logging.getLogger(__name__)


class LabPatient(models.Model):
    _inherit = 'lab.patient'

    patient_biomarker_ids = fields.One2many(
        comodel_name="lab.patient.biomarker",
        inverse_name="patient_id",
        string="Biomarkers"
    )