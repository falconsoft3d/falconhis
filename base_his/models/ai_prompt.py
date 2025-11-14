# -*- coding: utf-8 -*-
# Part of FalconHis. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, _

class AiPrompt(models.Model):
    _description = "AI Prompt"
    _name = 'ai.prompt'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'sequence, id'

    name = fields.Char('Name', required=True, tracking=True)
    sequence = fields.Integer('Sequence', default=10)
    active = fields.Boolean('Active', default=True, tracking=True)
    
    prompt_template = fields.Text(
        'Prompt Template', required=True, tracking=True,
        help="""Template for AI prompt. You can use the following variables:
- {patient_info}: Patient name
- {specialty}: Medical specialty
- {disease}: Associated disease
- {description}: Medical description from the record
        """)
    
    system_message = fields.Text(
        'System Message', required=True, tracking=True,
        help='System message that defines the AI behavior and role.')
    
    max_tokens = fields.Integer(
        'Max Tokens', default=800, required=True,
        help='Maximum number of tokens in the AI response.')
    
    temperature = fields.Float(
        'Temperature', default=0.7, required=True,
        help='Controls randomness: 0 is focused and deterministic, 1 is creative and random.')
    
    is_default = fields.Boolean(
        'Default Prompt', default=False, tracking=True,
        help='If checked, this prompt will be used by default for new medical records.')
    
    description = fields.Text('Description', help='Description of what this prompt is used for.')
    
    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env.company, required=True)

    @api.model_create_multi
    def create(self, vals_list):
        # If any prompt is set as default, unset other defaults
        for vals in vals_list:
            if vals.get('is_default'):
                self.search([('is_default', '=', True)]).write({'is_default': False})
                break
        return super().create(vals_list)

    def write(self, vals):
        # If this prompt is set as default, unset other defaults
        if vals.get('is_default'):
            self.search([('is_default', '=', True), ('id', 'not in', self.ids)]).write({'is_default': False})
        return super().write(vals)

    def action_set_as_default(self):
        """Set this prompt as the default one."""
        self.ensure_one()
        self.search([('is_default', '=', True)]).write({'is_default': False})
        self.is_default = True

    @api.model
    def get_default_prompt(self):
        """Get the default prompt or return the first active one."""
        default_prompt = self.search([('is_default', '=', True), ('active', '=', True)], limit=1)
        if not default_prompt:
            default_prompt = self.search([('active', '=', True)], limit=1)
        return default_prompt
