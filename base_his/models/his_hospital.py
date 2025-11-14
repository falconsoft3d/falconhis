# -*- coding: utf-8 -*-
# Part of FalconHis. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, _

class HisHospital(models.Model):
    _description = "His Hospital"
    _name = 'his.hospital'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Name')
    company_id = fields.Many2one('res.company', string='Company', required=True,
                                 default=lambda self: self.env.company)