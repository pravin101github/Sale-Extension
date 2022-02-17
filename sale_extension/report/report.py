from odoo import models
from datetime import datetime, timedelta
from odoo.tools.misc import str2bool, xlwt


class SaleorderXlsx(models.AbstractModel):
    _name = 'report.sale_extension.sale_order_xlsx'
    _inherit = 'report.report_xlsx.abstract'


    def get_customer_details(self,partner):
        customer_data=''
        if partner.name:
            customer_data += partner.name + '\n'
        if partner.street:
            customer_data += partner.street + '\n'
        if partner.street2:
            customer_data += partner.street2 + '\n'
        if partner.city:
            customer_data += partner.city + ' '
        if partner.state_id:
            customer_data += str(partner.state_id.code + ' ')
        if partner.zip:
            customer_data += partner.zip + ' '
        if partner.country_id:
            customer_data += '\n' + str(partner.country_id.name)
        if partner.phone:
            customer_data += '\n' + str(partner.phone)
        return  customer_data


    def generate_xlsx_report(self, workbook, data, Saleorder):
        for obj in Saleorder:
            report_name = obj.name
            # One sheet by sale order
            customer_data = ''

            #Add format for the sheet
            table_header_left = workbook.add_format(
                {'bg_color': 'black', 'align': 'left', 'font_size': 12,
                 'font_color': 'white'})
            table_row_left = workbook.add_format(
                {'align': 'left', 'font_size': 12, 'border': 1})
            table_header_right = workbook.add_format(
                {'bg_color': 'black', 'align': 'right', 'font_size': 12,
                 'font_color': 'white', 'border': 1})
            table_row_right = workbook.add_format(
                {'align': 'right', 'font_size': 12, 'border': 1})
            customer_header_format = workbook.add_format({
                'align': 'center', 'font_size': 13, 'bold': True, 'border': 1})
            customer_format = workbook.add_format({
                'align': 'center', 'font_size': 13, 'border': 1})
            table_left = workbook.add_format(
                {'align': 'left', 'bold': True, 'border': 1})
            table_right = workbook.add_format(
                {'align': 'right', 'bold': True, 'border': 1})

            worksheet = workbook.add_worksheet(obj.name)

            company_id = obj.company_id

            #Get Company Details
            if company_id.name:
                customer_data += company_id.name + '\n'
            if company_id.street:
                customer_data += company_id.street + '\n'
            if company_id.street2:
                customer_data += company_id.street2 + '\n'
            if company_id.city:
                customer_data += company_id.city + ' '
            if company_id.state_id:
                customer_data += str(company_id.state_id.code + ' ')
            if company_id.zip:
                customer_data += company_id.zip + ' '
            if company_id.country_id:
                customer_data += '\n' + str(company_id.country_id.name)

            worksheet.merge_range('A1:A4', customer_data, customer_format)

            # Get partner Details
            customer_data = self.get_customer_details(obj.partner_id)
            worksheet.merge_range('C6:C10', customer_data, customer_format)

            if obj.partner_shipping_id == obj.partner_invoice_id:
                # Get partner shipping Details
                customer_data = self.get_customer_details(obj.partner_shipping_id)
                worksheet.write('A6', 'Invoicing and shipping address:', customer_header_format)
                worksheet.merge_range('A7:A10', customer_data, customer_format)
                hide_some_column=True

            else:
                # Get partner shipping Details
                customer_data = self.get_customer_details(obj.partner_shipping_id)
                worksheet.write('A6', 'shipping address:', customer_header_format)
                worksheet.merge_range('A7:A10', customer_data, customer_format)

                # Get partner invoice Details
                customer_data = self.get_customer_details(obj.partner_invoice_id)
                worksheet.write('A12', 'Invoice address:', customer_header_format)
                worksheet.merge_range('A13:A16', customer_data, customer_format)
                hide_some_column=False

            if not hide_some_column:
                if obj.state not in ['draft', 'sent']:
                    worksheet.merge_range(
                        'A18:A19', 'Order #', customer_header_format)
                    worksheet.merge_range(
                        'B18:B19', obj.name, customer_format)
                else:
                    worksheet.merge_range(
                        'A18:A19', 'Quotation #', customer_header_format)
                    worksheet.merge_range(
                        'B18:B19', obj.name, customer_format)

                if obj.client_order_ref:
                    worksheet.write(
                        'A21', 'Your Reference', customer_header_format)
                    worksheet.write(
                        'A22', obj.client_order_ref, customer_format)

                    if obj.confirmation_date and obj.state not in ['draft', 'sent']:
                        worksheet.write(
                            'B21', 'Date Ordered', customer_header_format)
                        worksheet.write(
                            'B22', str(obj.confirmation_date.date()), customer_format)
                    else:
                        worksheet.write(
                            'B21', 'Quotation Date:', customer_header_format)
                        worksheet.write(
                            'B22', str(obj.date_order.date()), customer_format)
                    if obj.user_id.name:
                        worksheet.write(
                            'C21', 'Salesperson', customer_header_format)
                        worksheet.write(
                            'C22', obj.user_id.name, customer_format)

                    if obj.payment_term_id:
                        worksheet.write(
                            'D21', 'Payment Terms', customer_header_format)
                        worksheet.write(
                            'D22', obj.payment_term_id.name, customer_format)

                    if obj.validity_date and obj.state in ['draft', 'sent']:
                        worksheet.write(
                            'E21', 'Expiration Date', customer_header_format)
                        worksheet.write(
                            'E22', obj.validity_date, customer_format)

                else:

                    if obj.confirmation_date and obj.state not in ['draft', 'sent']:
                        worksheet.write(
                            'A21', 'Date Ordered', customer_header_format)
                        worksheet.write(
                            'A22', str(obj.confirmation_date.date()), customer_format)
                    else:
                        worksheet.write(
                            'A21', 'Quotation Date:', customer_header_format)
                        worksheet.write(
                            'A22', str(obj.date_order.date()), customer_format)

                    if obj.user_id.name:
                        worksheet.write(
                            'B21', 'Salesperson', customer_header_format)
                        worksheet.write(
                            'B22', obj.user_id.name, customer_format)

                    if obj.payment_term_id:
                        worksheet.write(
                            'C21', 'Payment Terms', customer_header_format)
                        worksheet.write(
                            'C22', obj.payment_term_id.name, customer_format)

                    if obj.validity_date and obj.state in ['draft', 'sent']:
                        worksheet.write(
                            'D21', 'Expiration Date', customer_header_format)
                        worksheet.write(
                            'D22', obj.validity_date, customer_format)
            else:
                if obj.state not in ['draft', 'sent']:
                    worksheet.merge_range(
                        'A13:A14', 'Order #', customer_header_format)
                    worksheet.merge_range(
                        'B13:B13', obj.name, customer_format)
                else:
                    worksheet.merge_range(
                        'A13:A14', 'Quotation #', customer_header_format)
                    worksheet.merge_range(
                        'B13:B14', obj.name, customer_format)

                if obj.client_order_ref:
                    worksheet.write(
                        'A15', 'Your Reference', customer_header_format)
                    worksheet.write(
                        'A16', obj.client_order_ref, customer_format)

                    if obj.confirmation_date and obj.state not in ['draft', 'sent']:
                        worksheet.write(
                            'B15', 'Date Ordered', customer_header_format)
                        worksheet.write(
                            'B16', str(obj.confirmation_date.date()), customer_format)
                    else:
                        worksheet.write(
                            'B15', 'Quotation Date:', customer_header_format)
                        worksheet.write(
                            'B16', str(obj.date_order.date()), customer_format)
                    if obj.user_id.name:
                        worksheet.write(
                            'C15', 'Salesperson', customer_header_format)
                        worksheet.write(
                            'C16', obj.user_id.name, customer_format)

                    if obj.payment_term_id:
                        worksheet.write(
                            'D15', 'Payment Terms', customer_header_format)
                        worksheet.write(
                            'D16', obj.payment_term_id.name, customer_format)

                    if obj.validity_date and obj.state in ['draft', 'sent']:
                        worksheet.write(
                            'E15', 'Expiration Date', customer_header_format)
                        worksheet.write(
                            'E16', obj.validity_date, customer_format)

                else:

                    if obj.confirmation_date and obj.state not in ['draft', 'sent']:
                        worksheet.write(
                            'A15', 'Date Ordered', customer_header_format)
                        worksheet.write(
                            'A16', str(obj.confirmation_date.date()), customer_format)
                    else:
                        worksheet.write(
                            'A15', 'Quotation Date:', customer_header_format)
                        worksheet.write(
                            'A16', str(obj.date_order.date()), customer_format)

                    if obj.user_id.name:
                        worksheet.write(
                            'B15', 'Salesperson', customer_header_format)
                        worksheet.write(
                            'B16', obj.user_id.name, customer_format)

                    if obj.payment_term_id:
                        worksheet.write(
                            'C15', 'Payment Terms', customer_header_format)
                        worksheet.write(
                            'C16', obj.payment_term_id.name, customer_format)

                    if obj.validity_date and obj.state in ['draft', 'sent']:
                        worksheet.write(
                            'D15', 'Expiration Date', customer_header_format)
                        worksheet.write(
                            'D16', obj.validity_date, customer_format)


            if not hide_some_column:
                row = 24
            else:
                row = 18
            worksheet.set_column('A:A', 40)
            worksheet.set_column('B:B', 15)
            worksheet.set_column('C:C', 15)
            worksheet.set_column('D:D', 15)
            worksheet.set_column('E:E', 15)
            worksheet.set_column('F:F', 15)

            group = self.env.user.has_group(
                'product.group_discount_per_so_line')
            display_discount = any([l.discount for l in obj.order_line])
            display_tax = any([l.tax_id for l in obj.order_line])
            worksheet.write(row, 0, 'Product', table_header_left)
            worksheet.write(row, 1, 'Quantity', table_header_right)
            worksheet.write(row, 2, 'Unit Price', table_header_right)
            if display_discount and group:
                worksheet.write(row, 3, 'Disc.%', table_header_right)
                if display_tax:
                    worksheet.write(row, 4, 'Taxes', table_header_right)
                    worksheet.write(row, 5, 'Amount', table_header_right)
                else:
                    worksheet.write(row, 4, 'Amount', table_header_right)
            elif display_tax:
                worksheet.write(row, 3, 'Taxes', table_header_right)
                worksheet.write(row, 4, 'Amount', table_header_right)
            else:
                worksheet.write(row, 3, 'Amount', table_header_right)
            row += 1

            for line in obj.order_line:
                worksheet.write(row, 0, line.name, table_row_left)
                worksheet.write(row, 1, line.product_uom_qty, table_row_right)
                worksheet.write(row, 2, line.price_unit, table_row_right)
                if display_discount and group:
                    worksheet.write(row, 3, line.discount, table_row_right)
                    if display_tax and line.tax_id:
                        worksheet.write(
                            row, 4, line.tax_id.name, table_row_right)
                        worksheet.write(
                            row, 5, line.price_subtotal, table_row_right)
                        row += 1
                    elif not line.tax_id and display_tax:
                        worksheet.write(row, 4, '0', table_row_right)
                        worksheet.write(
                            row, 5, line.price_subtotal, table_row_right)
                        row += 1
                    else:
                        worksheet.write(
                            row, 4, line.price_subtotal, table_row_right)
                        row += 1
                elif display_tax:
                    if display_tax and line.tax_id:
                        worksheet.write(
                            row, 3, line.tax_id.name, table_row_right)
                        worksheet.write(
                            row, 4, line.price_subtotal, table_row_right)
                        row += 1
                    elif not line.tax_id:
                        worksheet.write(row, 3, '0', table_row_right)
                        worksheet.write(
                            row, 4, line.price_subtotal, table_row_right)
                        row += 1
                    else:
                        worksheet.write(
                            row, 3, line.price_subtotal, table_row_right)
                        row += 1
                else:
                    worksheet.write(
                        row, 3, line.price_subtotal, table_row_right)
                    row += 1
            if display_discount and group and display_tax:
                worksheet.merge_range(row, 0, row, 5, '')
                worksheet.write(row + 1, 4, 'Untaxed Amount', table_left)
                worksheet.write(row + 1, 5, obj.amount_untaxed, table_right)
                worksheet.write(row + 2, 4, 'Taxes', table_left)
                worksheet.write(row + 2, 5, obj.amount_tax, table_right)
                worksheet.write(row + 3, 4, 'Total', table_left)
                worksheet.write(row + 3, 5, obj.amount_total, table_right)
            elif not group and not display_tax and not display_discount:
                worksheet.merge_range(row, 0, row, 3, '')
                worksheet.write(row + 1, 2, 'Subtotal', table_left)
                worksheet.write(row + 1, 3, obj.amount_untaxed, table_right)
                worksheet.write(row + 2, 2, 'Total', table_left)
                worksheet.write(row + 2, 3, obj.amount_total, table_right)
            elif not group and not display_tax:
                worksheet.merge_range(row, 0, row, 3, '')
                worksheet.write(row + 1, 2, 'Subtotal', table_left)
                worksheet.write(row + 1, 3, obj.amount_untaxed, table_right)
                worksheet.write(row + 2, 2, 'Total', table_left)
                worksheet.write(row + 2, 3, obj.amount_total, table_right)
            elif not display_tax and not display_discount:
                worksheet.merge_range(row, 0, row, 3, '')
                worksheet.write(row + 1, 2, 'Subtotal', table_left)
                worksheet.write(row + 1, 3, obj.amount_untaxed, table_right)
                worksheet.write(row + 2, 2, 'Total', table_left)
                worksheet.write(row + 2, 3, obj.amount_total, table_right)
            elif group and display_discount:
                worksheet.merge_range(row, 0, row, 4, '')
                worksheet.write(row + 1, 3, 'Subtotal', table_left)
                worksheet.write(row + 1, 4, obj.amount_untaxed, table_right)
                worksheet.write(row + 2, 3, 'Total', table_left)
                worksheet.write(row + 2, 4, obj.amount_total, table_right)
            elif display_tax:
                worksheet.merge_range(row, 0, row, 4, '')
                worksheet.write(row + 1, 3, 'Subtotal', table_left)
                worksheet.write(row + 1, 4, obj.amount_untaxed, table_right)
                worksheet.write(row + 2, 3, 'Taxes', table_left)
                worksheet.write(row + 2, 4, obj.amount_tax, table_right)
                worksheet.write(row + 3, 3, 'Total', table_left)
                worksheet.write(row + 3, 4, obj.amount_total, table_right)

            if obj.note:
                worksheet.write('A35', obj.note)
            if obj.payment_term_id.note:
                worksheet.write('A36', obj.payment_term_id.note)
            if obj.fiscal_position_id and obj.fiscal_position_id.sudo().note:
                worksheet.write('A37', obj.fiscal_position_id.sudo().note)
