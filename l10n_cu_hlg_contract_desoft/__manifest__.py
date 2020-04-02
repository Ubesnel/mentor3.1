# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Contract Desoft',
    'version': '1.0',
    'summary': 'Contract',
    'sequence': 30,
    'description': """
    Contract for sale and purchase

    """,
    'category': 'Sale',
    'website': 'http://www.desoft.cu',
    'author': "Desoft. Holguín. Cuba.",
    'images': [],
    'depends': ['l10n_cu_hlg_contract'],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_view.xml',
        'views/contract_type_view.xml',
        'views/contract_view.xml',
        'views/contract_service_sale_view.xml',
    ],
    'demo': [

    ],
    'qweb': [

    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
