{
    'name': 'Pedidos de comida',
    'version': '1.0',
    'category': 'pedidos',
    'summary': 'Pedidos de comida por internet',
    'application': True,
    'depends': [
        'mail',
    ],
    'data': [
        # SECURITY
        'security/ir.model.access.csv',
        # VIEWS
        'views/views_cliente.xml',
        'views/views.xml',
        # MENUS
        'views/menus.xml',
    ],
}