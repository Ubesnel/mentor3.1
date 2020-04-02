# -*- coding: utf-8 -*-
import base64
import logging
from StringIO import StringIO
from datetime import timedelta, datetime

from odoo import api, fields, models, _, tools
from odoo.exceptions import UserError, ValidationError
from odoo.tools import ustr

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.model
    def create(self, vals):
        res = super(ResPartner, self).create(vals)
        # archive_nro = 0
        # for partner in self.search([]):
        #     if partner.archive_nro:
        #         try:
        #             nro = int(partner.archive_nro)
        #             if nro > archive_nro:
        #                 archive_nro = nro
        #         except Exception:
        #             _logger.debug("Nro Archive not integer",
        #                           exc_info=True)
        # if archive_nro > 0:
        #     res.archive_nro = archive_nro
        return res

