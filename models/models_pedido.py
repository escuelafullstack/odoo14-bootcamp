from odoo import api, fields, models


class Pedido(models.Model):
    _name = 'pedidos.pedido'

    detalle_ids = fields.One2many(
        'pedidos.pedido.detalle',
        'pedido_id',
        string='Detalles',
    )
    fecha = fields.Date('Fecha del Pedido')


class PedidoDetalle(models.Model):
    _name = 'pedidos.pedido.detalle'

    pedido_id = fields.Many2one(
        'pedidos.pedido',
        string='pedido',
        required=True,
    )
    producto_id = fields.Many2one(
        'pedidos.producto',
        string='Producto',
        required=True,
    )
    cantidad = fields.Integer(
        string='Cantidad',
        default=1,
        required=True,
    )
    precio_unitario = fields.Float(
        related='producto_id.precio',
        string='Precio/Unidad',
    )
    total = fields.Float(
        'Total',
        compute='_compute_total',
    )

    @api.depends('producto_id', 'cantidad')
    def _compute_total(self):
        for record in self:
            record.total = record.cantidad * record.precio_unitario


