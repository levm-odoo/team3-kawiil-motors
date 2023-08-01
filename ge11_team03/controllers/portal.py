from odoo import http
from odoo.addons.portal.controllers import portal
from odoo.addons.portal.controllers.portal import pager as portal_pager
from odoo.http import request
from odoo.tools.translate import _

class CustomerPortal(portal.CustomerPortal):

    ## Domain
    def _prepare_tickets_domain(self, partner):
        return [ ('partner_id', '=', [partner.id]) ]
    
     ##  Portal configuration functions
    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        partner = request.env.user.partner_id

        Tickets = request.env['repair.order']
        if 'tickets_count' in counters:
            values['tickets_count'] = Tickets.search_count(self._prepare_tickets_domain(partner)) \
                if Tickets.check_access_rights('read', raise_exception=False) else 1
        else:
            values['tickets_count'] = 1
        print("TEST",values['tickets_count'])

        return values

    def _prepare_repair_portal_rendering_values(self, search, search_in, page=1, **kwargs):
        Tickets = request.env['repair.order']

        partner = request.env.user.partner_id
        values = self._prepare_portal_layout_values()

        url = "/my/tickets"
        domain = self._prepare_tickets_domain(partner)
        
        pager_values = portal_pager(
            url=url,
            total=Tickets.search_count([]),
            page=page,
            step=self._items_per_page,
            url_args={},
        )
        
        searchbar_inputs = {
                'all': {'label': _('All'), 'input': 'all', 'domain': []},
                'name': {'label': _('Name'), 'input': 'name', 'domain': [('name', 'like', search)]},
                'vin': {'label': _('VIN'), 'input': 'vin', 'domain': [('lot_id.name', 'like', search)]},
            }
        
        domain += searchbar_inputs[search_in]['domain']

            
        tickets = Tickets.search(domain, limit=self._items_per_page, offset=pager_values['offset'])


        values.update({
            'tickets': tickets.sudo(),
            'page_name': 'tickets',
            'pager': pager_values,
            'search':search,
            'search_in':search_in,
            'searchbar_inputs':searchbar_inputs,
            'default_url': url,
        })

        return values

    ##  Controllers
    @http.route(['/my/tickets', '/my/tickets/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_tickets(self, search="",search_in="all",**kwargs):
        values = self._prepare_repair_portal_rendering_values(search,search_in,**kwargs)
        
        return request.render("ge11_team03.portal_my_tickets", values)
    
    @http.route(['/my/tickets/new'], type='http', methods=['GET','POST'], auth="user", website=True)
    def portal_new_ticket(self, **kw):
        Lots = request.env['stock.lot']
        partner = request.env.user.partner_id
        lots = Lots.search_read([('registry_id.owner_id','=',partner.id)],['id','name','product_id'],[])
        if(request.httprequest.method == 'GET'):
            values = {'partner':partner,
                    'lots':lots}
            return request.render("ge11_team03.portal_new_ticket", values)
        
        elif(request.httprequest.method == 'POST'):
            specified_lot = next((lot for lot in lots if lot['id'] == int(kw['ticket_lot'])), None)
            print('TEST',specified_lot)
            product_id = specified_lot['product_id']
            product_uom = request.env['product.template'].browse(product_id[0]).uom_id.id
            request.env['repair.order'].create(
                {
                    'description':kw['ticket_description'],
                    'lot_id':kw['ticket_lot'],
                    'product_id':product_id[0],
                    'partner_id':partner.id,
                    'product_uom':product_uom
                }
                )
            return self.portal_my_tickets()
    
    @http.route(['/my/tickets/<int:ticket_id>'], type='http', auth="public", website=True)
    def portal_ticket_page(self, ticket_id, access_token=None, **kw):
        ticket_sudo = self._document_check_access('repair.order', ticket_id, access_token=access_token)
        partner = request.env.user.partner_id
        

        backend_url = f'/web#model={ticket_sudo._name}'\
                      f'&id={ticket_sudo.id}'\
                      f'&action={ticket_sudo._get_portal_return_action().id}'\
                      f'&view_type=form'
        values = {
            'ticket': ticket_sudo,
            'report_type': 'html',
            'backend_url': backend_url
        }

        values = self._get_page_view_values(
            ticket_sudo, access_token, values, "", False)

        return request.render('ge11_team03.tickets_portal_template', values)
