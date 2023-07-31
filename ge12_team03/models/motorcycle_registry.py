from odoo import api, fields, models

class MotorcycleRegistry(models.Model):
    _name="motorcycle.registry"
    _inherit='motorcycle.registry'

    user = fields.Many2one(comodel_name="res.users")

    @api.model_create_multi
    def create(self, vals_list):
        registries = super().create(vals_list) 

        for registry in registries:
            if (len(registry.env['res.users']._name_search(registry.owner_id.name)) == 0):
                registry.user = registry.env["res.users"].create(
                {"login": registry.owner_email, "name": registry.owner_id.name, "password" : "test-1", "email" : registry.owner_email}
                )
                registry.action_grant_access(registry.user)
                registry.send_email()
        return registries

    def action_grant_access(self, registry):
        """Grant the portal access to the partner.

        If the partner has no linked user, we will create a new one in the same company
        as the partner (or in the current company if not set).

        An invitation email will be sent to the partner.
        """
        self.ensure_one()

        group_portal = self.env.ref('base.group_portal')
        group_user = self.env.ref('base.group_user')

        user_sudo = registry.sudo()

        if not user_sudo.active or not False:
            user_sudo.write({'active': True, 'groups_id': [(4, group_portal.id), (3, group_user.id)]})
            user_sudo.partner_id.signup_prepare()

        return True

    def send_email(self):
        mail_template = self.env.ref('ge12_team03.email_template_new_user')
        mail_template.send_mail(self.id, force_send=True)
