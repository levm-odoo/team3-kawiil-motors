from collections import OrderedDict

from odoo import http
from odoo.addons.portal.controllers import portal
from odoo.addons.portal.controllers.portal import pager as portal_pager
from odoo.http import request
from odoo.tools.translate import _

class CustomerPortal(portal.CustomerPortal):
    def _update_is_public(self):
        context = request.env.context.copy()
        context.update({'is_public': True})
        request.env.context = context

    def _is_admin(self):
        partner = request.env.user.partner_id
        return (request.env.user.has_group("base.group_erp_manager") or request.env.user.id == partner.SUPERUSER_ID) 
    
    ## Domain
    def _prepare_motorcycles_domain(self, partner):
        return [ '|',('is_public','=',True),('owner_id', '=', [partner.id]) ]
    
    ##  Portal configuration functions
    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        partner = request.env.user.partner_id

        MotorcycleRegistry = request.env['motorcycle.registry']
        if 'registries_count' in counters:
            values['registries_count'] = MotorcycleRegistry.search_count(self._prepare_motorcycles_domain(partner)) \
                if MotorcycleRegistry.check_access_rights('read', raise_exception=False) else 0

        return values
    
    def _prepare_motorcycle_portal_rendering_values(self, search, search_in, page=1, **kwargs):
        MotorcycleRegistry = request.env['motorcycle.registry']

        partner = request.env.user.partner_id
        values = self._prepare_portal_layout_values()

        url = "/my/motorcycles"
        domain = self._prepare_motorcycles_domain(partner)
        
        pager_values = portal_pager(
            url=url,
            total=MotorcycleRegistry.search_count([]),
            page=page,
            step=self._items_per_page,
            url_args={},
        )
        
        searchbar_inputs = {
                'all': {'label': _('All'), 'input': 'all', 'domain': []},
                'country': {'label': _('Country'), 'input': 'country', 'domain': [('owner_id.country_id.name', 'like', search)]},
                'state': {'label': _('State'), 'input': 'state', 'domain': [('owner_id.state_id.name', 'like', search)]},
                'rider_name': {'label': _('Rider Name'), 'input': 'rider_name', 'domain': [('owner_id.name', 'like', search)]},
                'make': {'label': _('Motorcyle Make'), 'input': 'make', 'domain': [('make', 'like', search)]},
                'model': {'label': _('Motorcyle Model'), 'input': 'model', 'domain': [('model', 'like', search)]},
            }
        
        domain += searchbar_inputs[search_in]['domain']

            
        registries = MotorcycleRegistry.search(domain, limit=self._items_per_page, offset=pager_values['offset'])


        values.update({
            'motorcycles': registries.sudo(),
            'page_name': 'motorcycles',
            'pager': pager_values,
            'search':search,
            'search_in':search_in,
            'searchbar_inputs':searchbar_inputs,
            'default_url': url,
        })

        return values

    ##  Controllers
    @http.route(['/my/motorcycles', '/my/motorcycles/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_motorcycles(self, search="",search_in="all",**kwargs):
        values = self._prepare_motorcycle_portal_rendering_values(search,search_in,**kwargs)
        
        return request.render("ge08_team03.portal_my_motorcycles", values)
    
    @http.route(['/my/motorcycles/<int:motorcycle_id>'], type='http', auth="public", website=True)
    def portal_motorcycle_page(self, motorcycle_id, access_token=None, **kw):
        motorcycle_sudo = self._document_check_access('motorcycle.registry', motorcycle_id, access_token=access_token)
        partner = request.env.user.partner_id
        
        can_modify = (motorcycle_sudo.owner_id.id == partner.id) or self._is_admin()

        backend_url = f'/web#model={motorcycle_sudo._name}'\
                      f'&id={motorcycle_sudo.id}'\
                      f'&action={motorcycle_sudo._get_portal_return_action().id}'\
                      f'&view_type=form'
        values = {
            'motorcycle': motorcycle_sudo,
            'report_type': 'html',
            'backend_url': backend_url,
            'can_modify': can_modify
        }

        values = self._get_page_view_values(
            motorcycle_sudo, access_token, values, "", False)

        return request.render('ge08_team03.motorcycles_portal_template', values)
    
    @http.route(['/my/motorcycles/<int:motorcycle_id>/edit'], type='http', methods=['GET','POST'], auth="public", website=True)
    def portal_edit_motorcycle_page(self, motorcycle_id, access_token=None, **kw):
        if(request.httprequest.method == 'GET'):
            motorcycle_sudo = self._document_check_access('motorcycle.registry', motorcycle_id, access_token=access_token)

            backend_url = f'/web#model={motorcycle_sudo._name}'\
                        f'&id={motorcycle_sudo.id}'\
                        f'&action={motorcycle_sudo._get_portal_return_action().id}'\
                        f'&view_type=form'
            values = {
                'motorcycle': motorcycle_sudo,
                'report_type': 'html',
                'backend_url': backend_url,
            }

            values = self._get_page_view_values(
                motorcycle_sudo, access_token, values, "", False)

            return request.render('ge08_team03.motorcycles_edit_template', values)
        
        elif(request.httprequest.method == 'POST'):
            motorcycle_sudo = self._document_check_access('motorcycle.registry', motorcycle_id, access_token=access_token)
            
            if license_plate := kw.get('license_plate',False):
                motorcycle_sudo['license_plate'] = license_plate
            if current_mileage := kw.get('current_mileage',False):
                motorcycle_sudo['current_mileage'] = current_mileage

            motorcycle_sudo['is_public'] = kw.get('is_public',False)
            if not kw.get('is_public',False):
                return self.portal_my_motorcycles()
            return self.portal_motorcycle_page(motorcycle_id,access_token)
