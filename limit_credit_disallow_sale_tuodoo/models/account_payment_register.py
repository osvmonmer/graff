from collections import defaultdict
from lxml import etree

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.tools import float_compare, frozendict


class AccountPaymentRegister(models.TransientModel):
    _inherit = 'account.payment.register'

    def action_create_payments(self):
        vals = super(AccountPaymentRegister, self).action_create_payments()        
        amount_use = self.partner_id.amount_use
        amount_total = self.partner_id.amount_total
        print("++++++++++++++++++++++++++++++","action_create_payments",amount_use,amount_total)
        if amount_total > 0:
            self.partner_id.write({'amount_total': amount_total - self.amount,'amount_use': amount_use - self.amount})
        else:
            self.partner_id.write({'amount_total': amount_total + self.amount,'amount_use': amount_use - self.amount})
