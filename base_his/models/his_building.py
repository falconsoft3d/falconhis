# -*- coding: utf-8 -*-
# Part of FalconHis. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, _

class HisBuilding(models.Model):
    _description = "His Building"
    _name = 'his.building'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Name', translate=True)
    hospital_id = fields.Many2one(
        'his.hospital', string='Hospital', required=True, ondelete='cascade')