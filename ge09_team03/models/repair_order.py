from odoo import api, fields, models
from odoo.exceptions import ValidationError


class RepairOrder(models.Model):
    _inherit= "repair.order"

    current_mileage = fields.Float(string="Old Mileage", related="registry_id.current_mileage", compute="_compute_new_mileage", store=True)

    new_mileage = fields.Float(string="Current Mileage", readonly = False, store=True,)

    registry_id = fields.Many2one(comodel_name='motorcycle.registry',compute="_compute_registry_id", store=True)

    product_id = fields.Many2one(
        'product.product', string='Product to Repair',
        domain="[('type', 'in', ['product', 'consu']), '|', ('company_id', '=', company_id), ('company_id', '=', False)]",
        readonly=True, required=True, states={'draft': [('readonly', False)]}, check_company=True,store=True, related="registry_id.lot_id.product_id")

    product_type = fields.Selection(string="Product Type", related = "registry_id.lot_id.product_id.detailed_type")

    partner_id = fields.Many2one(
        'res.partner', 'Customer',
        index=True, states={'confirmed': [('readonly', True)]}, check_company=True, change_default=True,
        help='Choose partner for whom the order will be invoiced and delivered. You can find a partner by its Name, TIN, Email or Internal Reference.', related="registry_id.owner_id")
    
    repair_sale_order_id = fields.Many2one('sale.order', 'Sale Order', copy=False, store=True, related="registry_id.sale_order_id")
    

    @api.depends('lot_id')
    def _compute_registry_id(self):
        for repair in self:
            repair.registry_id = self.env['motorcycle.registry'].search([('vin', '=', repair.lot_id.name)])

    @api.depends('new_mileage')
    def _compute_new_mileage(self):
        for repair in self:
            repair.current_mileage = repair.new_mileage
