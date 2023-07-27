from odoo import http
from odoo.addons.portal.controllers import portal
from odoo.addons.portal.controllers.portal import pager as portal_pager
from odoo.http import request

class CustomerPortal(portal.CustomerPortal):
    def _update_is_public(self):
        context = request.env.context.copy()
        context.update({'is_public': True})
        request.env.context = context
    
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
    
    def _prepare_motorcycle_portal_rendering_values(self, page=1, **kwargs):
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
        registries = MotorcycleRegistry.search(domain, limit=self._items_per_page, offset=pager_values['offset'])

        values.update({
            'motorcycles': registries.sudo(),
            'page_name': 'motorcycles',
            'pager': pager_values,
            'default_url': url,
        })

        return values

    ##  Controllers
    @http.route(['/my/motorcycles', '/my/motorcycles/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_motorcycles(self, **kwargs):
        values = self._prepare_motorcycle_portal_rendering_values(**kwargs)
        
        return request.render("ge08_team03.portal_my_motorcycles", values)
    
    @http.route(['/my/motorcycles/<int:motorcycle_id>'], type='http', auth="public", website=True)
    def portal_motorcycle_page(self, motorcycle_id, report_type=None, access_token=None, download=False, **kw):
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

        return request.render('ge08_team03.motorcycles_portal_template', values)


