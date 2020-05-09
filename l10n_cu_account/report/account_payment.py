# -*- coding: utf-8 -*-

import time
from odoo import api, models

dicc = {
    '01': 'Enero',
    '02': 'Febrero',
    '03': 'Marzo',
    '04': 'Abril',
    '05': 'Mayo',
    '06': 'Junio',
    '07': 'Julio',
    '08': 'Agosto',
    '09': 'Septiembre',
    '10': 'Octubre',
    '11': 'Noviembre',
    '12': 'Diciembre',
}

class ReportPayment(models.AbstractModel):
    _name = 'report.l10n_cu_account.report_payment'

    def _get_month(self, docs):
        array = []
        result = ''
        for d in docs:
            date = d.payment_date.split('-')
            if array.count(dicc[date[1]]) == 0:
                array.append(dicc[date[1]])
        for a in array:
            result += a + ','
        return result

    def _get_year(self, docs):
        array = []
        result = ''
        for d in docs:
            date = d.payment_date.split('-')
            if array.count(date[0]) == 0:
                array.append(str(date[0]))
        for a in array:
            result += a + ','
        return result

    def _get_invoices(self, o):
        invoices = []
        for inv in o.invoice_ids:
            invoices.append(inv)
        return invoices

    @api.model
    def render_html(self, docids, data=None):
        user_name=self.env['res.users'].browse(self._uid).name
        docargs = {
            'docs': self.env['account.payment'].search([('id', '=', docids), ('state', '!=', 'draft')]),
            'time': time,
            'get_month': self._get_month,
            'get_year': self._get_year,
            'get_invoices': self._get_invoices,
            'user_name':user_name,
        }
        return self.env['report'].render('l10n_cu_account.report_payment', docargs)
