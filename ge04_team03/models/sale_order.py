from odoo import api,fields,models

class SaleOrder(models.Model):
    _inherit = ['sale.order']

    is_new_customer = fields.Boolean(
        default="True",
        compute="_check_new_customer",
        readonly=True
    )
    has_motorcycles = fields.Boolean(
        default="False",
        readonly=True
    )

    @api.depends('partner_id')
    def _check_new_customer(self):
        for order in self:
            # 1. Se buscan las SO del cliente
            partner_orders = order.env['sale.order'].search([('partner_id','=',order.partner_id.id)])
            # 2. Se identifican las SOLs que tienen productos con un detailed_type = motorcycle
            motorcycle_lines = partner_orders.mapped(
                lambda p_order: p_order.order_line.filtered(
                    lambda line: line.product_template_id.detailed_type == 'motorcycle'
                    )
                )
            order.is_new_customer = False if motorcycle_lines else True
    @api.onchange('order_line')
    def _has_ordered_motorcycles(self):
        self.has_motorcycles = True if self.order_line.filtered(lambda line: line.product_template_id.detailed_type == 'motorcycle') else False

    def apply_discount(self):
        # Asignación de la lista de precios con el descuento a la orden de compra
        self.pricelist_id = self.env.ref('ge04_team03.discount_pricelist')
        # Actualización del precio con el descuento
        self.action_update_prices()
