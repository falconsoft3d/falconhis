# -*- coding: utf-8 -*-
# Part of FalconHis. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, _

class HisRoom(models.Model):
    _description = "His Room"
    _name = 'his.room'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Name', translate=True)
    his_floor_id = fields.Many2one(
        'his.floor', string='Floor', required=True, ondelete='cascade')