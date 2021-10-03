import statistics

from odoo import api, fields, models

from .utils import (
    SELECTION_PEDIDO_ESTADO,
    PEDIDO_ESTADO_REGISTRO,
    PEDIDO_ESTADO_ENPREPARACION,
    PEDIDO_ESTADO_FINALIZADO,
)


class Pedido(models.Model):
    _name = 'pedidos.pedido'
    _inherit = 'mail.thread'
    _description = 'Pedido'
    _rec_name = 'cliente_id'

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
        tracking=True,
    )

    state = fields.Selection(
        SELECTION_PEDIDO_ESTADO,
        'Estado',
        default=PEDIDO_ESTADO_REGISTRO,
        tracking=True,
    )

    @api.onchange('cliente_id')
    def _onchange_cliente_id(self):
        self.direccion_id = False
        if len(self.cliente_id.direccion_ids) == 1:
            self.direccion_id = self.cliente_id.direccion_ids

        # Busqueda de pedidos anteriores
        if self.cliente_id:
            # Pedidos del cliente
            domain = [
                ('cliente_id', '=', self.cliente_id.id),  # Pedidos del cliente
                ('state', '=', PEDIDO_ESTADO_FINALIZADO),  # Que el pedido esté en finalizado
            ]
            pedido_objs = self.search(domain)

            # Detalles de los pedidos
            domain = [
                ('pedido_id', 'in', pedido_objs.ids),
            ]

            detalle_objs = self.env['pedidos.pedido.detalle'].search(domain)

            vals = {
                # producto1: [1,2,1]
                # producto2: [1,1,1]
            }

            for detalle in detalle_objs:
                if detalle.producto_id not in vals:
                    vals[detalle.producto_id] = []
                vals[detalle.producto_id].append(detalle.cantidad)

            val_detalle_ids = []

            for producto in vals:
                cantidad = statistics.mode(vals[producto])
                val = (0, 0, {'producto_id': producto.id, 'cantidad': cantidad})
                val_detalle_ids.append(val)

            self.detalle_ids = False
            self.detalle_ids = val_detalle_ids

            # Como llenar atributos one2many
            # https://www.odoo.com/es_ES/forum/ayuda-1/how-to-fill-one2many-field-134093

            print(vals)


    def action_enpreparacion(self):
        self.state = PEDIDO_ESTADO_ENPREPARACION

        for detalle in self.detalle_ids:
            producto = detalle.producto_id
            cantidad = detalle.cantidad

            '''
            producto.stock = producto.stock - cantidad
            producto.name = 'PIZZA DE CHAMPIÑONE'
            producto.fecha_vencimiento = '2021-12-12'

            # Esto no es optimo
            '''

            producto.sudo().write({
                'stock': producto.stock - cantidad,
                # 'name': 'PIZZA DE CHAMPIÑONE',
                # 'fecha_vencimiento': '2021-12-12',
            })

    def action_finalizar(self):
        self.state = PEDIDO_ESTADO_FINALIZADO


class PedidoDetalle(models.Model):
    _name = 'pedidos.pedido.detalle'
    _description = 'Detalle del pedido'

    pedido_id = fields.Many2one(
        'pedidos.pedido',
        string='pedido',
        required=True,
        index=True,
    )
    producto_id = fields.Many2one(
        'pedidos.producto',
        string='Producto',
        required=True,
        domain=[('stock', '>', 0)],
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
