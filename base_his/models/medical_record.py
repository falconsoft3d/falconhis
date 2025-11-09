# -*- coding: utf-8 -*-
# Part of FalconHis. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, _

class MedicalRecord(models.Model):
    _description = "Medical Record"
    _name = 'medical.record'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Name', default=lambda self: _('New'), readonly=True, copy=False)
    res_partner_id = fields.Many2one(
        'res.partner', string='Patient', required=True, ondelete='cascade')
    creation_date = fields.Datetime(
        'Creation Date', default=fields.Datetime.now, required=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', default=lambda self: self.env.user, required=True)
    description = fields.Text('Description', help='Additional information about the medical record.')
    medical_specialty_id = fields.Many2one(
        'medical.specialty', string='Medical Specialty', ondelete='set null')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('closed', 'Closed'),
    ], string='State', default='draft', tracking=True)

    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env.company, required=True)

    @api.model
    def create(self, vals_list):
        defaults = self.default_get(['requisition_type', 'company_id'])
        for vals in vals_list:
            company_id = vals.get('company_id', defaults['company_id'])
            vals['name'] = self.env['ir.sequence'].with_company(company_id).next_by_code(
                    'medical.record')
        return super().create(vals_list)

    def action_close(self):
        for record in self:
            record.state = 'closed'

    def action_set_draft(self):
        for record in self:
            record.state = 'draft'