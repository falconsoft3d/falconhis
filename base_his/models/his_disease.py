# -*- coding: utf-8 -*-
# Part of FalconHis. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError,ValidationError

class HisDisease(models.Model):
    _description = "His Disease"
    _name = 'his.disease'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    code = fields.Char('Code')
    name = fields.Char('Name')
    origin = fields.Char('Origin')
    description = fields.Text('Description')


    def create_description(self):
        """Generate AI description for the disease using OpenAI API."""
        for record in self:
            # Validate API key configuration
            ia_config = self.env['ia.config'].search([], limit=1)
            if not ia_config or not ia_config.api_key:
                raise UserError(_("AI API Key is not configured. Please configure it in Settings > IA Configurations."))
            
            # Validate that there is a disease name
            if not record.name or not record.name.strip():
                raise UserError(_("Disease name is required to generate a description."))
            
            # Build simple prompt
            disease_name = record.name
            disease_code = record.code if record.code else _("Not specified")
            
            prompt = f"""Proporciona una descripción médica profesional y concisa de la siguiente enfermedad:

Enfermedad: {disease_name}
Código: {disease_code}

Incluye en tu descripción:
1. Definición breve
2. Causas principales
3. Síntomas comunes
4. Tratamiento general

Mantén la descripción clara, profesional y en español."""
            
            try:
                import openai
                from openai import OpenAI
                
                # Initialize OpenAI client with API key
                client = OpenAI(api_key=ia_config.api_key)
                
                # Use the modern Chat Completions API
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "Eres un médico experto que proporciona descripciones médicas claras, precisas y profesionales de enfermedades. Siempre respondes en español."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=500,
                    temperature=0.7
                )
                
                record.description = response.choices[0].message.content.strip()
                
            except ImportError:
                raise UserError(_("Error: OpenAI library is not installed. Please install it using: pip install openai"))
            except openai.AuthenticationError:
                raise UserError(_("Error: Invalid API Key. Please check your API key configuration."))
            except openai.RateLimitError:
                raise UserError(_("Error: OpenAI API rate limit exceeded. Please try again later."))
            except openai.APIError as e:
                raise UserError(_("Error: OpenAI API error - %s") % str(e))
            except Exception as e:
                raise UserError(_("Error generating description: %s") % str(e))