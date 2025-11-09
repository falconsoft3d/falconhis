{
    'name': 'Base HIS MFH',
    'version' : '1.2',
    'summary': 'Hospital Information System',
    'sequence': 10,
    'description': """
Father (TOTP)
================================
Allows users to configure
    """,
    'category': 'Accounting/Accounting',
    'website': 'https://www.falconhis.com',
    'depends': ['base','mail','product'],
    'category': 'Extra Tools',
    'auto_install': False,
    'data': [
        'security/ir.model.access.csv',
        # Data
        'data/his_disease_data.xml',
        # Views inheritance
        'views/product_template_views.xml',
        # Views
        'views/his_disease_views.xml',
        'views/type_measurement_views.xml',
        'views/medical_specialty_views.xml',
        'views/menu_views.xml',
    ],
    'license': 'LGPL-3',
}