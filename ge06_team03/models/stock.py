from odoo import api, fields, models


class StockLot(models.Model):
    _inherit = 'stock.lot'
    
    name = fields.Char(compute="_compute_vin", store=True, default="New")
    serial_number = fields.Char(default="")
    manual = fields.Boolean(compute="_is_manual", default=True)
    serial_number_manual = fields.Char()

    
    @api.depends('product_id')
    def _compute_vin(self):
        for record in self:
            product_template = record.product_id.product_tmpl_id
            if(product_template.detailed_type == 'motorcycle'):
                if not isinstance(record.id, models.NewId):
                    record.serial_number = self.env['ir.sequence'].next_by_code('serial.number')
                record.name = product_template.make[0:2] + product_template.model[0:2] + str(product_template.year) + str(product_template.battery_capacity).upper() + record.serial_number
            else:
                record.name = record.name
    