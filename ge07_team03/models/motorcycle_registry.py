from odoo import api, fields, models
from odoo.exceptions import ValidationError

class MotorcycleRegistry(models.Model):
    _inherit = 'motorcycle.registry'
    
    lot_ids = fields.One2many('stock.lot',inverse_name='registry_id')
    lot_id = fields.Many2one('stock.lot',compute='compute_lot_id')
    sale_order_id = fields.Many2one('sale.order')
    
    vin = fields.Char(related="lot_id.name", required=False)
    owner_id = fields.Many2one("res.partner", ondelete="restrict", related="sale_order_id.partner_id")
    
    
    @api.depends('lot_ids')
    def compute_lot_id(self):
        self.lot_id=False
        if len(self.lot_ids) > 0:
            self.lot_id = self.lot_ids[0]
            
    @api.constrains('lot_ids')
    def _restrict_lot_count(self):
        if(len(self.lot_ids) > 2):
            print(type(self.lot_ids))
            raise ValidationError('A motorcycle registry can only have one lot assigned.')
        elif(self.lot_ids == False):
            raise ValidationError('A motorcycle registry must have an assigned lot')
