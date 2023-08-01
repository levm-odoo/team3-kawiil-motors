from odoo import http
from odoo.http import request


class SnippetControllers(http.Controller):
    
    @http.route(['/get_mileage'], type='json', auth="public", website=True)
    def get_mileage(self,**kw):
        registries = request.env['motorcycle.registry'].search([])
        mileage = 0
        for registry in registries:
            mileage+=registry.current_mileage
        return mileage
        
