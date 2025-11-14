# -*- coding: utf-8 -*-
# Part of FalconHis. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError,ValidationError

class TypeMeasurement(models.Model):
    _description = "Type Measurement"
    _name = 'type.measurement'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Name', translate=True)
    vital_sign = fields.Boolean('Vital Sign')