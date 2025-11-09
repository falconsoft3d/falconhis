# -*- coding: utf-8 -*-
# Part of FalconHis. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError,ValidationError

class HisDisease(models.Model):
    _description = "His Disease"
    _name = 'his.disease'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    code = fields.Char('Code', translate=True)
    name = fields.Char('Name', translate=True)
    origin = fields.Char('Origin')