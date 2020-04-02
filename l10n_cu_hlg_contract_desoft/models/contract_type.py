# -*- coding: utf-8 -*-
import base64
from StringIO import StringIO
from datetime import timedelta, datetime

from odoo import api, fields, models, _, tools
from odoo.exceptions import UserError, ValidationError
from odoo.tools import ustr


class ContractType(models.Model):
    _inherit = "l10n_cu_contract.contract_type"

    # TODO: Contract Support
    required_support_contract = fields.Boolean('Support Contract',
                                       help='',
                                       track_visibility='always')

