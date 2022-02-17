# -*- encoding: utf-8 -*-
from odoo import models, fields, api


class SaleConfiguration(models.TransientModel):
    _inherit = 'res.config.settings'

    group_product_product_visible = fields.Boolean('Manage Product Lines ', implied_group='sale_extension.group_product_product_visible',
                                                   defaults=True, readonly=False)
    group_product_template_visible = fields.Boolean('Manage Product Template',
                                                    implied_group='sale_extension.group_product_template_visible', dafault=False)

    @api.onchange('group_product_product_visible')
    def _onchange_group_product_configuration(self):
        '''set value as per change in configuration'''

        if self.group_product_product_visible:
            self.group_product_template_visible = False
        else:
            self.group_product_template_visible = True
