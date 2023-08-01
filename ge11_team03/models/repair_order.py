from odoo import fields,models

class RepairOrder(models.Model):
    _name="repair.order"
    _inherit = ['portal.mixin','repair.order']
    
    product_id = fields.Many2one(
        'product.product', string='Product to Repair',
        domain="[('type', 'in', ['product', 'consu']), '|', ('company_id', '=', company_id), ('company_id', '=', False)]",
        readonly=True, required=True, states={'draft': [('readonly', False)]}, check_company=True)


    def _compute_access_url(self):
        super()._compute_access_url()
        for ticket in self:
            ticket.access_url = f'/my/tickets/{ticket.id}'
            
            
    def _get_portal_return_action(self):
        self.ensure_one()
        return self.env.ref('repair.action_repair_order_tree')
