from odoo import api, fields, models

class MrpProduction(models.Model):
    _inherit = 'mrp.production'
    
    def action_confirm(self):
        super().action_confirm()
        for record in self:
            record.action_generate_serial()
