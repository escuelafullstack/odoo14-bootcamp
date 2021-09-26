from odoo import api, fields, models

from .utils import SELECTION_PEDIDO_ESTADO, PEDIDO_ESTADO_REGISTRO, PEDIDO_ESTADO_ENPREPARACION


class Pedido(models.Model):
    _name = 'pedidos.pedido'

    detalle_ids = fields.One2many(
        'pedidos.pedido.detalle',
        'pedido_id',
        string='Detalles',
    )
    fecha = fields.Date(
        'Fecha del Pedido',
        default=lambda self: fields.Date.context_today(self),
    )

    cliente_id = fields.Many2one(
        'pedidos.cliente',
        string='Cliente',
    )
    direccion_id = fields.Many2one(
        'pedidos.cliente.direccion',
        'Dirección de entrega',
    )

    state = fields.Selection(
        SELECTION_PEDIDO_ESTADO,
        'Estado',
        default=PEDIDO_ESTADO_REGISTRO,
    )

    @api.onchange('cliente_id')
    def _onchange_cliente_id(self):
        self.direccion_id = False
        if len(self.cliente_id.direccion_ids) == 1:
            self.direccion_id = self.cliente_id.direccion_ids

    def action_enpreparacion(self):
        self.state = PEDIDO_ESTADO_ENPREPARACION


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
            record.total = record.cantidad * record.precio_unitario * (1 - record.producto_id.descuento / 100.0)

