from odoo import api, fields, models
from re import findall as regex_findall, split as regex_split


class StockLot(models.Model):
    _inherit = 'stock.lot'
    
    name = fields.Char(compute='_compute_name', store=True)
    product_template = fields.Many2one(comodel_name='product.template', ondelete='restrict')
    make = fields.Char(related='product_template.make')
    model = fields.Char(related='product_template.model')
    
    @api.model_create_multi
    def create(self, vals_list):
        for record in self:
            product_template = record.product_id.product_tmpl_id
            record.vin = product_template.make[0:2]
        for vals in vals_list:
            if vals.get('name', ('New')) == ('New'):
                vals['name'] = self.make or "dump" + self.env['ir.sequence'].next_by_code('serial.number')
        return super().create(vals_list)
    
    
    # @api.depends('product_id')
    # def _compute_vin(self):
    #     self.vin = ""
    #     for record in self:
    #         serial_number = record._get_next_serial(record.company_id,record.product_id)
    #         product_template = record.product_id.product_tmpl_id
    #         if(product_template.detailed_type == 'motorcycle'):
    #             serial_number = str(record._get_next_serial(record.company_id,record.product_id))
    #             record.vin = product_template.make[0:2] + product_template.model[0:2] + str(product_template.year) + str(product_template.battery_capacity).upper() + serial_number
    #         else:
    #             record.vin = record.vin
                
                
    # @api.model
    # def generate_lot_names(self, first_lot, count):
    #     """Generate `lot_names` from a string."""
    #     # We look if the first lot contains at least one digit.
    #     caught_initial_number = regex_findall(r"\d+", first_lot)
    #     if not caught_initial_number:
    #         return self.generate_lot_names(first_lot + "0", count)


    #     # We base the series on the last number found in the base lot.
    #     initial_number = caught_initial_number[-1]
    #     padding = 7
    #     # We split the lot name to get the prefix and suffix.
    #     splitted = regex_split(initial_number, first_lot)
    #     # initial_number could appear several times, e.g. BAV023B00001S00001
    #     prefix = initial_number.join(splitted[:-1])
    #     suffix = splitted[-1]
    #     initial_number = int(initial_number)

    #     lot_names = []
    #     for i in range(0, count):
    #         lot_names.append(
    #             str(initial_number + i).zfill(padding),
    #         )
    #     return lot_names
    
    # @api.model
    # def _get_next_serial(self, company, product):
    #     """Return the next serial number to be attributed to the product."""
    #     if product.tracking != "none":
    #         last_serial = self.env['stock.lot'].search(
    #             [('company_id', '=', company.id), ('product_id', '=', product.id)],
    #             limit=1, order='id DESC')
    #         return last_serial.name
    #         if last_serial:
    #             print(last_serial.name)
    #             return self.env['stock.lot'].generate_lot_names(last_serial.name, 2)[1]
    #     return False
        