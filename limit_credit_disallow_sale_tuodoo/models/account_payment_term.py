from odoo import api, fields, models
from datetime import datetime, date


class AccountPaymentTerm(models.Model):
    _inherit = 'account.payment.term'

    term_days = fields.Integer(
        string='Dias',
        copy=False
    )
