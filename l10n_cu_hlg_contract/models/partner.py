# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class ResPartner(models.Model):
    _inherit = "res.partner"

    contract_count = fields.Integer(compute='_compute_contract_count', string='# of Contract')
    contract_ids = fields.One2many('sale.order', 'partner_id', 'Sales Order')

    @api.multi
    def name_get(self):
        res = []
        for record in self:
            name = record.name
            if record.reeup_code:
                name = record.reeup_code + '/' + name
            elif record.ci:
                name = record.ci + '/' + name
            else:
                name = record.name
            res.append((record.id, name))
        return res

    def _compute_contract_count(self):
        contract_data = self.env['l10n_cu_contract.contract'].read_group(domain=[('partner_id', 'child_of', self.ids)],
                                                      fields=['partner_id'], groupby=['partner_id'])
        # read to keep the child/parent relation while aggregating the read_group result in the loop
        partner_child_ids = self.read(['child_ids'])
        mapped_data = dict([(m['partner_id'][0], m['partner_id_count']) for m in contract_data])
        for partner in self:
            # let's obtain the partner id and all its child ids from the read up there
            partner_ids = filter(lambda r: r['id'] == partner.id, partner_child_ids)[0]
            partner_ids = [partner_ids.get('id')] + partner_ids.get('child_ids')
            # then we can sum for all the partner's child
            partner.contract_count = sum(mapped_data.get(child, 0) for child in partner_ids)




