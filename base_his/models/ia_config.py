# -*- coding: utf-8 -*-
# Part of FalconHis. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, _

class IaConfig(models.Model):
    _description = "Ia Config"
    _name = 'ia.config'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Name', translate=True)
    api_key = fields.Char('API Key', required=True)