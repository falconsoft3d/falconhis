# -*- coding: utf-8 -*-
# Part of FalconHis. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, _

class HisBed(models.Model):
    _description = "His Bed"
    _name = 'his.bed'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Name', translate=True)
    his_room_id = fields.Many2one(
        'his.room', string='Room', required=True, ondelete='cascade')