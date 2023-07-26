from odoo import api, fields, models

class MrpProduction(models.Model):
    _inherit = 'mrp.production'
    
    def action_generate_serial(self):
        self.ensure_one()
        self.lot_producing_id = self.env['stock.lot'].create(self._prepare_stock_lot_values())
        if self.product_id.tracking == 'serial':
            self.lot_producing_id['name']+"Test"
            print(self.lot_producing_id['name'])
            self._set_qty_producing()
    