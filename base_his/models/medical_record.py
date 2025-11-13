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

    product_id = fields.Many2one(
        'product.product', string='Service/Product', ondelete='set null',
        help='The medical service or product associated with this record.')

    creation_date = fields.Datetime(
        'Creation Date', default=fields.Datetime.now, required=True)
    user_id = fields.Many2one(
        'res.users', string='User', default=lambda self: self.env.user, required=True)
    description = fields.Text('Description', help='Additional information about the medical record.')
    ai_recommendation = fields.Text(
        'AI Recommendation', help='AI-generated recommendations for this medical record.')

    start_date = fields.Datetime('Start Date')
    end_date = fields.Datetime('End Date')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('started', 'Started'),
        ('finished', 'Finished'),
        ('cancelled', 'Cancelled')
    ], string='State', default='draft', tracking=True)

    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env.company, required=True)

    his_disease_id = fields.Many2one(
        'his.disease', string='Disease', ondelete='set null',
        help='The disease associated with this medical record.')
    
    ai_prompt_id = fields.Many2one(
        'ai.prompt', string='AI Prompt Template', ondelete='set null',
        help='The AI prompt template to use for generating recommendations.')

    his_mass_billing_id = fields.Many2one(
        'his.mass.billing', string='Mass Billing', ondelete='set null',
        help='The mass billing associated with this medical action.')

    quantity = fields.Float('Quantity', default=1.0, help='Quantity of the medical product.')
    price_unit = fields.Float('Unit Price', help='Unit price of the medical product.')
    amount = fields.Float('Amount', help='Monetary amount associated with this medical action.',
                          compute='_compute_amount', store=True)

    currency_id = fields.Many2one(
        'res.currency', string='Currency', required=True,
        default=lambda self: self.env.company.currency_id)

    @api.depends('quantity', 'price_unit')
    def _compute_amount(self):
        for record in self:
            record.amount = record.quantity * record.price_unit

    @api.onchange('product_id', 'price_unit', 'quantity')
    def _onchange_product_id(self):
        for record in self:
            record.price_unit = record.product_id.list_price


    def action_open_prompt_wizard(self):
        """Open wizard to select AI prompt before generating recommendation."""
        self.ensure_one()
        
        # Get default prompt if not set
        if not self.ai_prompt_id:
            default_prompt = self.env['ai.prompt'].get_default_prompt()
            if default_prompt:
                self.ai_prompt_id = default_prompt
        
        return {
            'name': _('Select AI Prompt'),
            'type': 'ir.actions.act_window',
            'res_model': 'medical.record',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new',
            'context': {'form_view_ref': 'base_his.view_form_medical_record_prompt_wizard'},
        }

    def action_generate_ai_recommendation(self):
        """Generate AI recommendations using OpenAI's latest API with selected prompt."""
        for record in self:
            # Validate API key configuration
            ia_config = self.env['ia.config'].search([], limit=1)
            if not ia_config or not ia_config.api_key:
                record.ai_recommendation = _("AI API Key is not configured. Please configure it in Settings.")
                continue
            
            # Validate that there is a description to analyze
            if not record.description or not record.description.strip():
                record.ai_recommendation = _("No description available to generate recommendations.")
                continue
            
            # Get the prompt template to use
            prompt_template = record.ai_prompt_id
            if not prompt_template:
                prompt_template = self.env['ai.prompt'].get_default_prompt()
            
            if not prompt_template:
                record.ai_recommendation = _("No AI Prompt template configured. Please create one in Configuration > AI Prompts.")
                continue
            
            # Build context variables
            patient_info = record.res_partner_id.name if record.res_partner_id else _("Unknown Patient")
            specialty = record.medical_specialty_id.name if record.medical_specialty_id else _("General")
            disease = record.his_disease_id.name if record.his_disease_id else _("Not specified")
            
            # Format the prompt with variables
            prompt = prompt_template.prompt_template.format(
                patient_info=patient_info,
                specialty=specialty,
                disease=disease,
                description=record.description
            )
            
            try:
                import openai
                from openai import OpenAI
                
                # Initialize OpenAI client with API key
                client = OpenAI(api_key=ia_config.api_key)
                
                # Use the modern Chat Completions API with prompt configuration
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",  # or "gpt-4" for better results
                    messages=[
                        {"role": "system", "content": prompt_template.system_message},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=prompt_template.max_tokens,
                    temperature=prompt_template.temperature
                )
                
                record.ai_recommendation = response.choices[0].message.content.strip()
                
            except ImportError:
                record.ai_recommendation = _("Error: OpenAI library is not installed. Please install it using: pip install openai")
            except openai.AuthenticationError:
                record.ai_recommendation = _("Error: Invalid API Key. Please check your API key configuration.")
            except openai.RateLimitError:
                record.ai_recommendation = _("Error: OpenAI API rate limit exceeded. Please try again later.")
            except openai.APIError as e:
                record.ai_recommendation = _("Error: OpenAI API error - %s") % str(e)
            except KeyError as e:
                record.ai_recommendation = _("Error: Invalid prompt template. Missing variable: %s") % str(e)
            except Exception as e:
                record.ai_recommendation = _("Error generating recommendation: %s") % str(e)

    @api.model
    def create(self, vals_list):
        defaults = self.default_get(['requisition_type', 'company_id'])
        for vals in vals_list:
            company_id = vals.get('company_id', defaults['company_id'])
            vals['name'] = self.env['ir.sequence'].with_company(company_id).next_by_code(
                    'medical.record')
        return super().create(vals_list)

    def action_to_start(self):
        for record in self:
            record.start_date = fields.Datetime.now()
            record.state = 'started'

    def action_to_finish(self):
        for record in self:
            record.end_date = fields.Datetime.now()
            record.state = 'finished'

    def action_set_draft(self):
        for record in self:
            record.state = 'draft'