#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Part of FalconHis. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models

class ResPartner(models.Model):
    _inherit = 'res.partner'

    type_of_gender = fields.Selection([
        ('M', 'Male'),
        ('F', 'Female')
    ], 'Gender', size=1, default='M')

    patient = fields.Boolean('Is a Patient', default=True)

    """ Medial Records """
    medical_record_ids = fields.One2many('medical.record', 'res_partner_id', 'Medical Record')
    medical_record_count = fields.Integer('Medical Records', compute="_get_medical_record_count")

    room_id = fields.Many2one(
        'his.room', string='To Room', ondelete='set null',
        help='The room to which the patient is moving.')

    @api.depends('medical_record_ids')
    def _get_medical_record_count(self):
        for partner in self:
            partner.medical_record_count = len(partner.medical_record_ids)

    def action_view_medical_records(self):
        self.ensure_one()
        return {
            'name': 'Medical Records',
            'type': 'ir.actions.act_window',
            'res_model': 'medical.record',
            'view_mode': 'list,form',
            'domain': [('res_partner_id', '=', self.id)],
            'context': {'default_res_partner_id': self.id}
        }

    """ Medical Actions """
    medical_action_ids = fields.One2many('medical.action', 'res_partner_id', 'Medical Actions')
    medical_action_count = fields.Integer('Medical Actions', compute="_get_medical_action_count")

    @api.depends('medical_action_ids')
    def _get_medical_action_count(self):
        for partner in self:
            partner.medical_action_count = len(partner.medical_action_ids)

    def action_view_medical_actions(self):
        self.ensure_one()
        return {
            'name': 'Medical Actions',
            'type': 'ir.actions.act_window',
            'res_model': 'medical.action',
            'view_mode': 'list,form',
            'domain': [('res_partner_id', '=', self.id)],
            'context': {'default_res_partner_id': self.id}
        }




