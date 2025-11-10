# -*- coding: utf-8 -*-
# Part of FalconHis. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, _

class PatientMovement(models.Model):
    _description = "Patient Movement"
    _name = 'patient.movement'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    name = fields.Char('Name', default=lambda self: _('New'), readonly=True, copy=False)
    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env.company, required=True)

    user_id = fields.Many2one(
        'res.users', string='User', default=lambda self: self.env.user, required=True
    )

    res_partner_id = fields.Many2one(
        'res.partner', string='Patient', required=True, ondelete='cascade',
        help='The patient associated with this movement.')

    type_of_movement = fields.Selection([
        ('admission', 'Admission'),
        ('transfer', 'Transfer'),
        ('discharge', 'Discharge')
    ], string='Type of Movement', required=True, tracking=True, default='admission')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], string='State', default='draft', tracking=True)

    description = fields.Text('Description', help='Additional information about the patient movement.')

    creation_date = fields.Datetime(
        'Creation Date', default=fields.Datetime.now, required=True)

    from_his_room_id = fields.Many2one(
        'his.room', string='From Room', ondelete='set null',
        help='The room from which the patient is moving.')

    to_his_room_id = fields.Many2one(
        'his.room', string='To Room', ondelete='set null',
        help='The room to which the patient is moving.')

    @api.model
    def create(self, vals_list):
        defaults = self.default_get(['requisition_type', 'company_id'])
        for vals in vals_list:
            company_id = vals.get('company_id', defaults['company_id'])
            vals['name'] = self.env['ir.sequence'].with_company(company_id).next_by_code('patient.movement')
        return super().create(vals_list)

    def action_complete_movement(self):
        for record in self:
            record.state = 'completed'
            if record.type_of_movement in ['admission', 'transfer']:
                record.res_partner_id.room_id = record.to_his_room_id
            elif record.type_of_movement == 'discharge':
                record.res_partner_id.room_id = False

    def action_cancel_movement(self):
        for record in self:
            record.state = 'cancelled'

    def action_set_draft(self):
        for record in self:
            record.state = 'draft'