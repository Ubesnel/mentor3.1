# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
import json
from odoo.tools import float_is_zero
from odoo.exceptions import UserError, RedirectWarning, ValidationError
from datetime import datetime


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    signed_date = fields.Date('Signed Date')
    folio = fields.Char('Folio')
    name_related = fields.Char('Number', related='name', store=True, readonly=True, copy=False)
    date_invoice = fields.Date(string='Invoice Date',
                               readonly=True, states={'draft': [('readonly', False)]},
                               index=True,
                               help="Keep empty to use the current date", copy=False,
                               default=fields.Date.today())

    @api.multi
    def action_invoice_open(self):
        if not self.signed_date:
            raise UserError(
                _('Signed date is not defined'))
        super(AccountInvoice, self).action_invoice_open()

        for inv in self:
            if inv.name:
                inv.number = inv.name

    @api.one
    @api.depends('payment_move_line_ids.amount_residual')
    def _get_payment_info_JSON(self):
        self.payments_widget = json.dumps(False)
        if self.payment_move_line_ids:
            info = {'title': _('Less Payment'), 'outstanding': False, 'content': []}
            currency_id = self.currency_id
            for payment in self.payment_move_line_ids:
                payment_currency_id = False
                if self.type in ('out_invoice', 'in_refund'):
                    amount = sum(
                        [p.amount for p in payment.matched_debit_ids if p.debit_move_id in self.move_id.line_ids])
                    amount_currency = sum([p.amount_currency for p in payment.matched_debit_ids if
                                           p.debit_move_id in self.move_id.line_ids])
                    if payment.matched_debit_ids:
                        payment_currency_id = all([p.currency_id == payment.matched_debit_ids[0].currency_id for p in
                                                   payment.matched_debit_ids]) and payment.matched_debit_ids[
                                                  0].currency_id or False
                elif self.type in ('in_invoice', 'out_refund'):
                    amount = sum(
                        [p.amount for p in payment.matched_credit_ids if p.credit_move_id in self.move_id.line_ids])
                    amount_currency = sum([p.amount_currency for p in payment.matched_credit_ids if
                                           p.credit_move_id in self.move_id.line_ids])
                    if payment.matched_credit_ids:
                        payment_currency_id = all([p.currency_id == payment.matched_credit_ids[0].currency_id for p in
                                                   payment.matched_credit_ids]) and payment.matched_credit_ids[
                                                  0].currency_id or False
                # get the payment value in invoice currency
                if payment_currency_id and payment_currency_id == self.currency_id:
                    amount_to_show = amount_currency
                else:
                    amount_to_show = payment.company_id.currency_id.with_context(date=payment.date).compute(amount,
                                                                                                            self.currency_id)
                if float_is_zero(amount_to_show, precision_rounding=self.currency_id.rounding):
                    continue

                if payment.payment_id:
                    payment_ref = payment.payment_id.name

                info['content'].append({
                    'name': payment.name,
                    'journal_name': payment.journal_id.name,
                    'amount': amount_to_show,
                    'currency': currency_id.symbol,
                    'digits': [69, currency_id.decimal_places],
                    'position': currency_id.position,
                    'date': payment.date,
                    'payment_id': payment.id,
                    'move_id': payment.move_id.id,
                    'ref': payment_ref,
                })
            self.payments_widget = json.dumps(info)

    @api.multi
    def action_invoice_paid(self):
        # lots of duplicate calls to action_invoice_paid, so we remove those already paid
        to_pay_invoices = self.filtered(lambda inv: inv.state != 'paid')
        if to_pay_invoices.filtered(lambda inv: inv.state not in ['open', 'conciliate', 'claimed', 'efectoxcobrar']):
            raise UserError(_('Invoice must be validated in order to set it to register payment.'))
        if to_pay_invoices.filtered(lambda inv: not inv.reconciled):
            raise UserError(
                _('You cannot pay an invoice which is partially paid. You need to reconcile payment entries first.'))
        return to_pay_invoices.write({'state': 'paid'})

    @api.multi
    def _write(self, vals):
        pre_not_reconciled = self.filtered(lambda invoice: not invoice.reconciled)
        pre_reconciled = self - pre_not_reconciled
        res = super(AccountInvoice, self)._write(vals)
        reconciled = self.filtered(lambda invoice: invoice.reconciled)
        not_reconciled = self - reconciled
        (reconciled & pre_reconciled).filtered(
            lambda invoice: invoice.state in ['done', 'conciliate', 'claimed', 'efectoxcobrar']).action_invoice_paid()
        (not_reconciled & pre_not_reconciled).filtered(lambda invoice: invoice.state == 'paid').action_invoice_re_open()
        return res

    @api.model
    def send_email_invoice(self):
        days = 21

        # para los contratos cercanos a la fecha de vencimiento
        template = self.env.ref('l10n_cu_account.mail_template_data_notification_invoice2')
        contract_array = []
        invoices = self.env['account.invoice'].search([
            ('state', 'not in', ['cancel', 'paid', 'draft']),
            ('type', '=', 'out_invoice')
        ])
        for invoice in invoices:
            if invoice.signed_date:
                time_validez = datetime.today() - datetime.strptime(invoice.signed_date, '%Y-%m-%d')
                if time_validez.days >= 0:
                    if time_validez.days >= days:
                        if invoice.partner_id.email and invoice.partner_id.email != 'None':
                            dicc = {
                                'email_to': invoice.partner_id.email
                            }
                            template.with_context(dbname=self._cr.dbname, record=invoice.id).send_mail(invoice.id, force_send=True,
                                                                                             email_values=dicc)


        return True
