from odoo import api, fields, models

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    #name=fields.Char(compute='_compute_name_prefix')

    
    battery_capacity = fields.Selection(selection=[('xs','Small'),
                                        ('0m','Medium'),
                                        ('0l','Larga'),
                                        ('xl','Extra Large'),],
                                        copy=False
                                       )
    charge_time = fields.Float()
    curb_weight = fields.Float()
    horsepower = fields.Float()
    launch_date = fields.Date()
    make = fields.Char()
    model = fields.Char()
    range = fields.Float()
    top_speed = fields.Float()
    torque = fields.Float()
    year = fields.Integer()
    
    detailed_type = fields.Selection(selection_add=[('motorcycle','Motorcycle')], 
                            ondelete={'motorcycle': 'set product'},
                            help='A storable product is a product for which you manage stock. The Inventory app has to be installed.\n'
                            'A consumable product is a product for which stock is not managed.\n'
                            'A service is a non-material product you provide.\n'
                            'A motorcycle is a captivating symbol of freedom, power, and adventure, offering an exhilarating two-wheeled escape that combines speed, agility, and the thrill of the open road.')

    type = fields.Selection(selection_add=[('motorcycle','Motorcycle')], 
                            ondelete={'motorcycle': 'set product'},
                            help='A storable product is a product for which you manage stock. The Inventory app has to be installed.\n'
                            'A consumable product is a product for which stock is not managed.\n'
                            'A service is a non-material product you provide.\n'
                            'A motorcycle is a captivating symbol of freedom, power, and adventure, offering an exhilarating two-wheeled escape that combines speed, agility, and the thrill of the open road.')


    def _detailed_type_mapping(self):
        type_mapping = super()._detailed_type_mapping()
        type_mapping['motorcycle'] = 'product'
        return type_mapping
    
    #@api.depends('year', 'make', 'model')
    #def _create_name_prefix(self):
    #    for record in self:
    #        if (record.detailed_type == 'motorcycle'):
    #            record.name = '[' + str(record.year) + str(record.make) + str(record.model) + ']' + ' ' + str(record.name)
    #        else:
    #            record.name=record.name

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if (vals.detailed_type == 'motorcycle'):
                vals.name = '[' + str(vals.year) + str(vals.make) + str(vals.model) + ']' + ' ' + str(vals.name)
            return super().create(vals_list)
        
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('detailed_type', ('motorcyle')) == ('motorcycle'):
                vals['name'] = '[' + str(vals['year']) + str(vals['make']) + str(vals['model']) + ']' + ' ' + str(vals['name'])
        return super().create(vals_list)