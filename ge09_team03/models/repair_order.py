from odoo import api, fields, models
from odoo.exceptions import ValidationError


class RepairMotorcycle(models.Model):
    _inherit= "repair.order"

    registry_id = fields.Many2one(comodel_name='motorcycle.registry',compute="_compute_registry_id", store=True)

    product_id = fields.Many2one(
        'product.product', string='Product to Repair',
        domain="[('type', 'in', ['product', 'consu']), '|', ('company_id', '=', company_id), ('company_id', '=', False)]",
        readonly=True, required=True, states={'draft': [('readonly', False)]}, check_company=True,store=True, compute="_compute_product_id")

    partner_id = fields.Many2one(
        'res.partner', 'Customer',
        index=True, states={'confirmed': [('readonly', True)]}, check_company=True, change_default=True,
        help='Choose partner for whom the order will be invoiced and delivered. You can find a partner by its Name, TIN, Email or Internal Reference.', compute="_compute_owner")
    
    repair_sale_order_id = fields.Many2one('sale.order', 'Sale Order', copy=False, store=True, compute="_compute_sale_order")
    

    @api.depends('lot_id')
    def _compute_registry_id(self):
        for lot in self:
            lot.registry_id = self.env['motorcycle.registry'].search([('vin', '=', lot.lot_id.name)])

    @api.depends('registry_id')
    def _compute_product_id(self):
        for lot in self:
            if(lot.registry_id.model):
                lot.product_id = self.env['product.product'].search([('model', '=', lot.registry_id.model)])
            else:
                lot.product_id = False

    @api.depends('registry_id')
    def _compute_owner(self):
        for lot in self:
            if(lot.registry_id.owner_id):
                lot.partner_id = self.env['res.partner'].search([('name', '=', lot.registry_id.owner_id.name)])
            else:
                lot.partner_id = False

    @api.depends('registry_id')
    def _compute_sale_order(self):
        for lot in self:
            if(lot.registry_id.sale_order_id):
                lot.repair_sale_order_id = self.env['sale.order'].search([('name', '=', lot.registry_id.sale_order_id.name)])
                print(lot.repair_sale_order_id)
            else:
                lot.repair_sale_order_id = False
