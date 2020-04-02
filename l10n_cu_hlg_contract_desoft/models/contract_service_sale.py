# -*- coding: utf-8 -*-
import base64
from StringIO import StringIO
from datetime import timedelta, datetime

from odoo import api, fields, models, _, tools
from odoo.exceptions import UserError, ValidationError
from odoo.tools import ustr


class ContractServiceSale(models.Model):
    _name = "l10n_cu_contract.contract_service_sale"

    _rec_name = 'code'

    code = fields.Char(string='Code', required=True)
    name = fields.Char(string='Name', required=True)
    company_id = fields.Many2one('res.company', string='Company', index=True,
                                 default=lambda self: self.env.user.company_id)
    color = fields.Integer('Color Index', default=0)
    contract_ids = fields.One2many('l10n_cu_contract.contract', 'service_id', string='Contracts')
    count_contract = fields.Integer(string='Contracts Count', compute='_compute_count_contract')

    @api.one
    @api.depends('contract_ids')
    def _compute_count_contract(self):
        self.count_contract = len(self.contract_ids)

