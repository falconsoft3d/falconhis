# -*- coding: utf-8 -*-
# Part of FalconHis. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, _

class MedicalAction(models.Model):
    _description = "Medical Action"
    _name = 'medical.action'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    name = fields.Char('Name', default=lambda self: _('New'), readonly=True, copy=False)
    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env.company, required=True)

    res_partner_id = fields.Many2one(
        'res.partner', string='Patient', required=True, ondelete='cascade',
        help='The patient associated with this medical action.')

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

    state = fields.Selection([
        ('draft', 'Draft'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], string='State', default='draft', tracking=True)

    product_id = fields.Many2one(
        'product.product', string='Product', ondelete='set null',
        help='The medical product associated with this action.')

    description = fields.Text('Description', help='Additional information about the medical action.')

    file_attachment_ids = fields.Many2many(
        'ir.attachment', string='Attachments',
        help='Attach relevant files or documents related to this medical action.')

    value = fields.Char('Value', help='Value associated with the medical action.')

    creation_date = fields.Datetime(
        'Creation Date', default=fields.Datetime.now, required=True)
    planning_date = fields.Datetime(
        'Planning Date', help='Scheduled date and time for the medical action.')
    execution_date = fields.Datetime(
        'Execution Date', help='Date and time when the medical action was executed.')

    user_id = fields.Many2one('res.users', string='User', default=lambda self: self.env.user, required=True)
    exec_user_id = fields.Many2one('res.users', string='User Exec', default=lambda self: self.env.user, required=True)

    @api.model
    def create(self, vals_list):
        defaults = self.default_get(['requisition_type', 'company_id'])
        for vals in vals_list:
            company_id = vals.get('company_id', defaults['company_id'])
            vals['name'] = self.env['ir.sequence'].with_company(company_id).next_by_code('medical.action')
        return super().create(vals_list)

    def action_complete(self):
        for record in self:
            record.exec_user_id = self.env.user
            record.state = 'completed'
            record.execution_date = fields.Datetime.now()

    def action_set_draft(self):
        for record in self:
            record.state = 'draft'

    def action_cancel(self):
        for record in self:
            record.state = 'cancelled'