from odoo import models, fields, api

class todos(models.Model):
    _name = 'lab.patient.biomarker'
    _description = 'Patient biomarkers'

    patient_id = fields.Many2one('lab.patient', string='Patient', required=True)

    biomarkers = fields.Char(string="Biomarkers")

    @api.model
    def patient_biomarker_tracing(self, biomarker):
        print(biomarker)
        biomarker_model = self.env["lab.patient.biomarker"]
        biomarker_model.create({
            "patient_id": 2,
            "biomarkers": str(biomarker)
        })


