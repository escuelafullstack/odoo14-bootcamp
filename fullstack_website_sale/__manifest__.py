{
    'name': 'Website Sale - Fullstack',
    'version': '1.0',
    'category': 'website',
    'summary': 'Website Sale',
    'application': True,
    'depends': [
        'base_geolocalize',
        'website_sale',
    ],
    'data': [
        # DATA
        'data/data.xml',

        # VIEWS
        'views/website_sale_templates.xml',
    ],
}