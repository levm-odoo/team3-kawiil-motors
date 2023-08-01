from odoo import models

class RepairOrder(models.Model):
    _name="repair.order"
    _inherit = ['portal.mixin','repair.order']


    def _compute_access_url(self):
        super()._compute_access_url()
        for ticket in self:
            ticket.access_url = f'/my/tickets/{ticket.id}'
            
    def _get_portal_return_action(self):
        self.ensure_one()
        return self.env.ref('repair.action_repair_order_tree')
