# -*- coding: utf-8 -*-
import base64
import logging
from StringIO import StringIO
from datetime import timedelta, datetime

from odoo import api, fields, models, _, tools
from odoo.exceptions import UserError, ValidationError
from odoo.tools import ustr

_logger = logging.getLogger(__name__)


class Contract(models.Model):
    _inherit = "l10n_cu_contract.contract"

    national_contract = fields.Boolean('National Contract', default=False, help="")
    nro_national_contract = fields.Char('Nro National Contract')
    required_support_contract = fields.Boolean(related='contract_type.required_support_contract')
    contract_id = fields.Many2one('l10n_cu_contract.contract', 'Contract')
    service_id = fields.Many2one('l10n_cu_contract.contract_service_sale', string='Product or Service')