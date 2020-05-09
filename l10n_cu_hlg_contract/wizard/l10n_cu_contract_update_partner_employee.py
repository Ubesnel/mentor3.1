# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import logging
from odoo import models, api
from odoo.exceptions import ValidationError
from odoo.tools.translate import _

_logger = logging.getLogger(__name__)

resp_dic = {'nokey': _('You must request a registry key. Please contact the support center for a new one.'),
            'invalidkey': _('You are using a invalid key. Please contact the support center for a new one.'),
            'expkey': _('You are using a expired key. Please contact the support center for a new one.'),
            'invalidmod': _('You are using a invalid key. Please contact the support center for a new one.')}


class UpdatePartnerEmployee(models.TransientModel):
    _name = "l10n_cu_contract.update_partner_employee"

    @api.multi
    def update_partner_employee(self):
        data = {}

        # check_reg
        resp = self.env['l10n_cu_base.reg'].check_reg('l10n_cu_contract')
        if resp != 'ok':
            raise ValidationError(resp_dic[resp])

        # TODO:CHECK VARIUS EMPLOYEES WITH THE SAME USER
        for emp in self.env['hr.employee'].search([]):
            job = '-'
            if emp.user_id:
                partner_id = emp.user_id.partner_id.id
                if emp.job_id:
                    job = emp.job_id.name
                partner = self.env['res.partner'].browse(partner_id)
                partner.write({'employee': True,
                               'customer': False,
                               'function': job,
                               'email': emp.work_email,
                               'notify_email': 'always',
                               'user_id': emp.user_id.id,
                               'ci': emp.identification_id,
                               })

        return True
