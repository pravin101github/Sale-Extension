# -*- coding: utf-8 -*-
from odoo import models, fields, api,_


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    product_tmpl_id = fields.Many2one('product.template','Product Template' ,domain=[('sale_ok', '=', True)])

    @api.model
    def create(self, values):
        '''override create method set product teml id'''
        if 'product_id' in values:
            product_rec = self.env['product.product'].browse(
                values['product_id'])
            if product_rec:
                values['product_tmpl_id'] = product_rec.product_tmpl_id.id
        return super(SaleOrderLine, self).create(values)

    @api.multi
    def write(self, values):
        '''override create method set product teml id'''
        if 'product_id' in values:
            product_rec = self.env['product.product'].browse(
                values['product_id'])
            if product_rec:
                values['product_tmpl_id'] = product_rec.product_tmpl_id.id
        return super(SaleOrderLine, self).write(values)

    @api.multi
    @api.onchange('product_id')
    def product_id_change(self):
        """Override this to set product template id """
        res = super(SaleOrderLine, self).product_id_change()

        if self.product_id and not self.product_tmpl_id:
            self.product_tmpl_id = self.product_id.product_tmpl_id.id

        return res

    @api.multi
    @api.onchange('product_tmpl_id')
    def product_tmpl_id_change(self):
        """copy main product id onchange method make changes as per when select product templ id """
        if not self.product_tmpl_id:
            return {'domain': {'product_uom': []}}
        else:
            if self.product_tmpl_id:
                product_id = self.env['product.product'].search(
                    [('product_tmpl_id', '=', self.product_tmpl_id.id)],limit=1)

            vals = {}
            domain = {'product_uom': [
                ('category_id', '=', product_id.uom_id.category_id.id)]}
            if not self.product_uom or \
                    (product_id.uom_id.id != self.product_uom.id):
                vals['product_id'] = product_id.id
                vals['product_uom'] = product_id.uom_id
                vals['product_uom_qty'] = 1.0

            product = product_id.with_context(
                lang=self.order_id.partner_id.lang,
                partner=self.order_id.partner_id.id,
                quantity=vals.get('product_uom_qty') or self.product_uom_qty,
                date=self.order_id.date_order,
                pricelist=self.order_id.pricelist_id.id,
                uom=self.product_uom.id
            )

            result = {'domain': domain}
            self.product_id_change()

            title = False
            message = False
            warning = {}
            if product.sale_line_warn != 'no-message':
                title = _("Warning for %s") % product.name
                message = product.sale_line_warn_msg
                warning['title'] = title
                warning['message'] = message
                result = {'warning': warning}
                if product.sale_line_warn == 'block':
                    product_id = False
                    return result
            if product:
                name = product.name_get()[0][1]
                if product.description_sale:
                    name += '\n' + product.description_sale
                vals['name'] = name

            self._compute_tax_id()

            if self.order_id.pricelist_id and self.order_id.partner_id:
                vals['price_unit'] = self.env[
                    'account.tax']._fix_tax_included_price_company(
                    self._get_display_price(
                        product), product.taxes_id,
                    self.tax_id,
                    self.company_id)
            self.update(vals)

            return result






class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def action_quotation_send_excel(self):
        '''
        This function opens a window to compose an email, with the edi sale excel template message loaded by default
        '''
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        template_id = ir_model_data.get_object_reference('sale_extension', 'email_template_edi_sale_excel')[1]

        try:
            template_id = ir_model_data.get_object_reference('sale_extension', 'email_template_edi_sale_excel')[1]

        except ValueError:
            template_id = False
        try:
            compose_form_id = ir_model_data.get_object_reference('mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False
        lang = self.env.context.get('lang')
        template = template_id and self.env['mail.template'].browse(template_id)
        if template and template.lang:
            lang = template._render_template(template.lang, 'sale.order', self.ids[0])
        ctx = {
            'default_model': 'sale.order',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
            'model_description': self.with_context(lang=lang).type_name,
            'custom_layout': "mail.mail_notification_paynow",
            'proforma': self.env.context.get('proforma', False),
            'force_email': True
        }
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }









