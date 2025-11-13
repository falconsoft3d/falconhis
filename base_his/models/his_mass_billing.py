# -*- coding: utf-8 -*-
# Part of FalconHis. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, _

class HisMassBilling(models.Model):
    _description = "His Mass Billing"
    _name = 'his.mass.billing'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    name = fields.Char('Name', default=lambda self: _('New'), readonly=True, copy=False)
    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env.company, required=True)

    res_partner_id = fields.Many2one(
        'res.partner', string='Patient', required=True, ondelete='cascade',
        help='The patient associated with this medical action.')

    account_move_id = fields.Many2one(
        'account.move', string='Invoice', ondelete='set null',
        help='The invoice generated from this mass billing.')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('loaded', 'Loaded'),
        ('invoiced', 'Invoiced'),
        ('cancelled', 'Cancelled'),
    ], string='State', default='draft', tracking=True)

    user_id = fields.Many2one(
        'res.users', string='User',
        default=lambda self: self.env.user, tracking=True)

    creation_date = fields.Datetime(
        string='Creation Date', default=fields.Datetime.now, tracking=True)

    line_ids = fields.One2many(
        'his.mass.billing.line', 'his_mass_billing_id', string='Billing Lines',
        help='Lines of medical products/services to be billed in this mass billing.')

    @api.model
    def create(self, vals_list):
        for vals in vals_list:
            company_id = vals.get('company_id') or self.env.company.id
            vals['name'] = self.env['ir.sequence'].with_company(company_id).next_by_code('his.mass.billing')
        return super().create(vals_list)

    def action_load_data(self):
        """Load medical actions for the patient into billing lines."""
        self.ensure_one()

        # medical.action
        MedicalAction = self.env['medical.action']
        actions = MedicalAction.search([
            ('res_partner_id', '=', self.res_partner_id.id),
            ('his_mass_billing_id', '=', False),
            ('state', 'in', ['completed'])
        ])
        lines = []
        for action in actions:
            lines.append((0, 0, {
                'product_id': action.product_id.id,
                'origin': action.name,
                'quantity': action.quantity,
                'unit_price': action.price_unit,
                'amount': action.quantity * action.price_unit,
            }))

            action.his_mass_billing_id = self.id
        self.line_ids = lines


        # medical.record
        MedicalRecord = self.env['medical.record']
        records = MedicalRecord.search([
            ('res_partner_id', '=', self.res_partner_id.id),
            ('his_mass_billing_id', '=', False),
            ('state', 'in', ['finished'])
        ])
        for record in records:
            lines.append((0, 0, {
                'product_id': record.product_id.id,
                'origin': record.name,
                'quantity': record.quantity,
                'unit_price': record.price_unit,
                'amount': record.quantity * record.price_unit,
            }))

            record.his_mass_billing_id = self.id
        self.line_ids = lines

        self.state = 'loaded'

    def action_set_draft(self):
        for record in self:
            record.state = 'draft'

        # eliminamos las líneas asociadas
        self.line_ids.unlink()

        # medical.action
        # desasociamos las acciones médicas
        MedicalAction = self.env['medical.action']
        actions = MedicalAction.search([
            ('his_mass_billing_id', '=', self.id)
        ])
        for action in actions:
            action.his_mass_billing_id = False

        # medical.record
        # desasociamos los registros médicos
        MedicalRecord = self.env['medical.record']
        records = MedicalRecord.search([
            ('his_mass_billing_id', '=', self.id)
        ])
        for record in records:
            record.his_mass_billing_id = False

    def action_create_invoice(self):
        """Create invoice from billing lines."""
        self.ensure_one()
        AccountMove = self.env['account.move']
        AccountMoveLine = self.env['account.move.line']

        invoice_vals = {
            'move_type': 'out_invoice',
            'partner_id': self.res_partner_id.id,
            'company_id': self.company_id.id,
            'invoice_date': fields.Date.today(),
            'invoice_origin': self.name,
        }
        invoice = AccountMove.create(invoice_vals)

        for line in self.line_ids:
            line_vals = {
                'move_id': invoice.id,
                'product_id': line.product_id.id,
                'quantity': line.quantity,
                'price_unit': line.unit_price,
                'name': line.product_id.name,
            }
            AccountMoveLine.create(line_vals)

        # invoice.action_post()
        self.account_move_id = invoice.id

        self.state = 'invoiced'
        return invoice

    def action_to_loaded(self):
        for record in self:
            # eliminamos la factura asociada
            self.account_move_id.unlink()
            self.account_move_id = False
            record.state = 'loaded'


class HisMassBillingLine(models.Model):
    _description = "His Mass Billing Line"
    _name = 'his.mass.billing.line'

    his_mass_billing_id = fields.Many2one(
        'his.mass.billing', string='Mass Billing', required=True, ondelete='cascade')

    product_id = fields.Many2one(
        'product.product', string='Product', ondelete='set null',
        help='The medical product associated with this billing line.')

    origin = fields.Char('Origin', help='Origin of the billing line (e.g., medical action reference).')

    quantity = fields.Float('Quantity', default=1.0, required=True)
    unit_price = fields.Float('Unit Price', required=True)
    amount = fields.Float('Amount', compute='_compute_amount', store=True)


    def _compute_amount(self):
        for line in self:
            line.amount = line.quantity * line.unit_price