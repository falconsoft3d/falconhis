# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import _, api, fields, models

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    medical_type = fields.Selection(
        [('M', 'Medication'),
         ('E', 'Diagnostic_test'),
         ('P', 'Procedure'),
         ('T', 'Treatment'),
         ('C', 'Consultation'),
         ('V', 'Vaccine'),
         ('S', 'Service'),
         ('X', 'Other')
         ], string='Medical Type', help='Type of medical product', default='M')

    """
    | Spanish        | English             | Description / Usage |
    |----------------|--------------------|---------------------|
    | Medicamento    | `medication`       | Any prescribed drug, supply, or pharmaceutical product. |
    | Examen         | `laboratory_test`  | Laboratory or diagnostic tests (blood, imaging, etc.). |
    | Procedimiento  | `procedure`        | Medical, surgical, or technical interventions. |
    | Tratamiento    | `treatment`        | Therapy sessions or ongoing care (e.g., physiotherapy, chemotherapy). |
    | Consulta       | `consultation`     | Doctor visit or medical check-up. |
    | Vacuna         | `vaccine`          | Immunization doses or vaccinations. |
    | Servicio       | `service`          | Non-clinical services (e.g., ambulance, room, nursing). |
    """