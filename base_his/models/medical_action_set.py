# -*- coding: utf-8 -*-
# Part of FalconHis. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, _

class MedicalActionSet(models.Model):
    _description = "Medical Action Set"
    _name = 'medical.action.set'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    name = fields.Char('Name', required=True, tracking=True)
    description = fields.Text('Description', help='Description of this action set.')
    
    line_ids = fields.One2many(
        'medical.action.set.line', 'action_set_id', 
        string='Action Lines', copy=True)
    
    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env.company, required=True)


class MedicalActionSetLine(models.Model):
    _description = "Medical Action Set Line"
    _name = 'medical.action.set.line'
    _order = 'id'

    action_set_id = fields.Many2one('medical.action.set', string='Action Set', required=True, ondelete='cascade')
    medical_type = fields.Selection(
        [('M', 'Medication'),
         ('E', 'Test'),
         ('N', 'Measurement'),
         ('P', 'Procedure'),
         ('T', 'Treatment'),
         ('C', 'Consultation'),
         ('V', 'Vaccine'),
         ('S', 'Service'),
         ('X', 'Other')
         ], string='Medical Type', help='Type of medical product', default='M')
    product_id = fields.Many2one('product.product', string='Product', required=True, ondelete='restrict')
