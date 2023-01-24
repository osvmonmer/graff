# -*- coding: utf-8 -*-

from odoo import api, fields, models
from datetime import datetime, date


class ResPartner(models.Model):
    _inherit = 'res.partner'

    amount_limit = fields.Float(
        string='Credito',
        copy=False,
        tracking=True,
    )
    amount_use = fields.Float(
        string='Credito en uso',
        copy=False,
    )
    amount_total = fields.Float(
        string='Credito restante',
        copy=False,
    )

    active_credit = fields.Boolean(
        string="Activar credito",
    )

    @api.onchange('amount_limit')
    def onchange_amount_limit(self):
        for rec in self:
            if rec.amount_limit > 0:
                rec.amount_total = rec.amount_limit