# -*- coding: utf-8 -*-
# Part of FalconHis. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, _

class MedicalSpecialty(models.Model):
    _description = "Medical Specialty"
    _name = 'medical.specialty'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Name')