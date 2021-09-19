from odoo import fields, models


class Cliente(models.Model):
    _name = 'pedidos.cliente'
    _description = 'Cliente'

    documento = fields.Char('Doc.Identidad', required=True, size=8)
    name = fields.Char('Apellidos y nombres', required=True, size=100)
    telefono = fields.Char('Telefono', size=9)

    direccion_ids = fields.One2many(
        'pedidos.cliente.direccion',
        'cliente_id',
        string='Direcciones',
    )


class Direccion(models.Model):
    _name = 'pedidos.cliente.direccion'
    _description = 'Direcciones del cliente'

    cliente_id = fields.Many2one(
        'pedidos.cliente',
        string='Cliente',
    )

    name = fields.Char('Lugar', required=True)
    direccion = fields.Char('Dirección', required=True)
