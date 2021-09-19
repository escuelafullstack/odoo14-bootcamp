from odoo import fields, models


class Producto(models.Model):
    _name = 'pedidos.producto'

    name = fields.Char(
        string='Nombre del producto',
        required=True,
        size=100,
    )
    stock = fields.Integer('Stock')
    precio = fields.Float('Precio')
