# -*- coding: utf-8 -*-
# Part of FalconHis. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, _

class HisFloor(models.Model):
    _description = "His Floor"
    _name = 'his.floor'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Name', translate=True)
    his_building_id = fields.Many2one(
        'his.building', string='Building', required=True, ondelete='cascade')