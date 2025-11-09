#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Part of FalconHis. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models

class ResPartner(models.Model):
    _inherit = 'res.partner'

    type_of_gender = fields.Selection(
        [('M', 'Male'),
         ('F', 'Female')],
        'Gender', size=1, default='M')




