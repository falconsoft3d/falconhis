{
    'name': 'Base HIS MFH',
    'version' : '1.2',
    'summary': 'Hospital Information System',
    'author': 'Marlon Falcón Hernández',
    'sequence': 10,
    'description': """
Father (TOTP)
================================
Allows users to configure
    """,
    'category': 'Accounting/Accounting',
    'website': 'https://www.falconhis.com',
    'depends': ['base','base_setup','mail','product','account'],
    'category': 'Extra Tools',
    'auto_install': False,
    'data': [
        'security/ir.model.access.csv',
        # Data
        'data/his_disease_data.xml',
        'data/ir_sequence.xml',
        'data/ai_prompt_data.xml',
        # Views inheritance
        'views/product_template_views.xml',
        'views/res_partner_views.xml',
        # Views
        'views/his_disease_views.xml',
        'views/type_measurement_views.xml',
        'views/medical_specialty_views.xml',
        'views/his_hospital_views.xml',
        'views/his_building_views.xml',
        'views/his_floor_views.xml',
        'views/his_room_views.xml',
        'views/his_bed_views.xml',
        'views/medical_record_views.xml',
        'views/medical_action_views.xml',
        'views/medical_action_set_views.xml',
        'views/patient_movement_views.xml',
        'views/ia_config_views.xml',
        'views/ai_prompt_views.xml',
        'views/his_mass_billing_views.xml',
        'views/menu_views.xml',
    ],
    'license': 'LGPL-3',
}