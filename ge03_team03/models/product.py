from odoo import api, fields, models

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    name=fields.Char(compute='_compute_name_prefix',readonly=False,store= True)

    @api.depends('year', 'make', 'model')
    def _compute_name_prefix(self):
        for record in self:
            if ((record.detailed_type == 'motorcycle') and ((record.year != False) and (record.make !=False) and (record.model !=False))):
                record.name = '[' + str(record.year) + str(record.make) + str(record.model) + ']' + ' ' + str(record.name)
            else:
                record.name=record.name
                