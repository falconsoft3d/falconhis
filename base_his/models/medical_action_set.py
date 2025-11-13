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
    partner_id = fields.Many2one(
        'res.partner', string='Partner',
        help='Partner associated with this action set.')
    
    line_ids = fields.One2many(
        'medical.action.set.line', 'action_set_id', 
        string='Action Lines', copy=True)
    
    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env.company, required=True)

    def create_data(self):
        for line in self.line_ids:
            self.env['medical.action'].create({
                'res_partner_id': self.partner_id.id,
                'medical_type': line.medical_type,
                'product_id': line.product_id.id,
                'value': line.value,
                'price_unit': line.product_id.lst_price,
                'user_id': self.env.user.id,
                'planning_date': fields.Datetime.now(),
                'execution_date': fields.Datetime.now(),
                'state': 'completed',
            })
            line.value = ""
        self.partner_id = None
        self.message_post(body=_("Medical actions created from action set."))



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
    value = fields.Float('Value', help='Value associated with this action line.')
