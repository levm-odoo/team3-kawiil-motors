from odoo import api,fields,models

LOCATIONS = [
        # San Francisco
        {
            'states':[
                'California',
                'Nevada',
                'Arizona',
                'Utah',
                'New Mexico',
                'Texas',
                'Oregon',
                'Washington',
                'Montana',
                'Wyoming',
                'Colorado',
                'Oklahoma',
                'Kansas',
                'Alaska'

            ],
            'warehouse_id': 4
        },
        # Buffalo
        {
            'states':[
                'Arkansas',
                'Lousiana',
                'Missisipi',
                'Alabama',
                'Missouri',
                'Iowa',
                'South Dakota',
                'North Dakota',
                'Nebraska',
                'Minessota',
                'Wisconsin',
                'Illinois',
                'Indiana',
                'Tenesse',
                'Kentucky',
                'Georgia',
                'Florida',
                'Michigan',
                'South Carolina',
                'North Carolina',
                'Ohio',
                'Pensilvania',
                'Delaware',
                'New Yersey',
                'New York',
                'Vermont',
                'New Hampshire',
                'Connecticut',
                'Massachusets',
                'Maine'
            ],
            'warehouse_id': 3
        }
    ]

class SalesOrder(models.Model):
    _inherit = ["sale.order"]

    warehouse_id = fields.Many2one(
        comodel_name="stock.warehouse",
        compute="_compute_warehouse_id"
    )

    @api.depends('partner_shipping_id')
    def _compute_warehouse_id(self):
        for order in self:
            # Asignación de warehouse por defecto
            order.warehouse_id = self.env['stock.warehouse'].browse(4)
            
            for location in LOCATIONS:
                if order.partner_shipping_id.state_id.name in location['states']:
                    order.warehouse_id = self.env['stock.warehouse'].browse(location['warehouse_id'])
                    break
