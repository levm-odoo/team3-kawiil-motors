from odoo import api, Command, fields, models

class Picking(models.Model):
    _inherit = 'stock.picking'
    
    def _action_done(self):
        validation = super()._action_done()
        if(validation):
            for move_line in self.move_ids.move_line_ids:
                lot = move_line.lot_id
            
                if(lot.product_id.product_tmpl_id.detailed_type == 'motorcycle' and self.location_dest_id == self.env.ref("stock.stock_location_customers")):
                    sale_order = self.env['sale.order'].search([('name','=',self.origin)],limit=1)[0].id
                    print(lot.id, "LOT ID:")
                    self.env['motorcycle.registry'].create(
                        {
                            'lot_ids': [Command.link(lot.id)],
                            'sale_order_id': sale_order
                        })
                
        return validation
