# -*- coding: utf-8 -*-

{
    'name': 'Account',
    'summary': '',
    'description': """

""",

    'author': "Desoft. Holguín. Cuba.",
    'website': "www.desoft.cu",

    # Categories can be used to filter modules in modules listing.
    # Check /odoo/addons/base/module/module_data.xml for the full list.
    'category': 'account',
    'version': '1.0',
    # Any module necessary for this one to work correctly.
    'depends': ['account', 'payment'],

    # Always loaded.
    'data': [
        #'security/ir.model.access.csv',
        'report/report_payment.xml',
        'report/account_report.xml',

        'views/account_payment_view.xml',
        'views/account_invoice_view.xml',

        'data/ir_cron_data.xml',
        'data/invoice_template_data.xml',
        #'views/account_view.xml',
        #'views/open_chart.xml',
        ],

    # Only loaded in demonstration mode.
    'demo': [
    ],
    'qweb': [
    ],

    'test': [
    ],

    'installable': True,
    'application': True,
    'auto_install': False,
}

