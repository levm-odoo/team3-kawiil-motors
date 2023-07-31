from odoo import api, fields, models
from odoo.exceptions import ValidationError


class MotorcycleRegistry(models.Model):
    _inherit = "motorcycle.registry"

    current_mileage = fields.Float(related="repair_ids.new_mileage",store = True)

    repair_ids = fields.One2many("repair.order", inverse_name="registry_id", string="ID Order")

    repair_count = fields.Integer('Repair order count', compute='_compute_order_ids')

    @api.depends('repair_ids')
    def _compute_order_ids(self):
        for order in self:
            order.repair_count = len(order.repair_ids)
            
    def action_view_repair(self):
        return self._get_action_view_repair(self.repair_ids)

    def _get_action_view_repair(self, repairs):
        action = self.env["ir.actions.actions"]._for_xml_id("repair.action_repair_order_tree")

        if len(repairs) >= 1:
            action['domain'] = [('id', 'in', repairs.ids)]
        elif len(repairs) < 1:
            form_view = [(self.env.ref('repair.view_repair_order_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state,view) for state,view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = repairs.id
        return action
