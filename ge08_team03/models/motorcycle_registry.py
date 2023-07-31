from odoo import fields, models
from odoo.tools.translate import _

class MotorcycleRegistry(models.Model):
    _name="motorcycle.registry"
    _inherit = ['portal.mixin','motorcycle.registry',]
    
    is_public = fields.Boolean(default=False)

    def _compute_access_url(self):
        super()._compute_access_url()
        for motorcycle in self:
            motorcycle.access_url = f'/my/motorcycles/{motorcycle.id}'
            
    def _compute_edit_url(self):
        for motorcycle in self:
            motorcycle.access_url = f'/my/motorcycles/{motorcycle.id}/edit'
            
    def _get_portal_return_action(self):
        self.ensure_one()
        return self.env.ref('motorcycle_registry.registry_list_action')

        
