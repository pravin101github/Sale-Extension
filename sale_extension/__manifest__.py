{
    'name': "sale_extension",
    'summary': """
        This module used to Provide extension to sale module""",
    'description': """
        Ability To Print Excel Report on Quotation/ sales order
        Ability To Add new customized widget to float and integer fields
        we use this widget with integer or float field in form,tree view or report that field
        should display a "₹" sign before it.
        In the Quotation/ sales order we have an option to add product lines. We have to control
        those lines to come either from product_product OR product_template model.
    """,
    'author': "Pravin Jewale",
    'category': 'Sale',
    'version': '12.2',
    'depends': ['sale','base','contacts','sale_management','report_xlsx'],
    'demo': [
        'demo/demo.xml',
    ],
    'data': [
        'views/assets.xml',
        'views/sale_views.xml',
        'views/templates.xml',
        'views/res_config_view.xml',
        'report/sale_report.xml',
    ],

    'application':True
}
