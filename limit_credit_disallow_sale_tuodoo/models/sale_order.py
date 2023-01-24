# -*- coding: utf-8 -*-

from odoo import api, fields, models
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    state = fields.Selection([
        ('draft', 'Quotation'),
        ('sent', 'Quotation Sent'),
        ('locked', 'Bloqueado'),
        ('sale', 'Sales Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
        ], string='Status', readonly=True, copy=False, index=True, tracking=3, default='draft')

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        vals = super(SaleOrder, self).onchange_partner_id()
        print("+++++++++++++++++++++++",self.partner_id.amount_use)
        self.amount_limit_total = self.partner_id.amount_total
        if self.partner_id.amount_limit == 0:
            self.limit_state = 'blocked'
        return vals

    amount_limit_total = fields.Float(
        string='Credito disponible',
        copy=False,
    )

    limit_state = fields.Selection([
        ('done', 'Green'),
        ('blocked', 'Red')], string='Credito',
        copy=False, default='done',compute='_compute_amount_cal')

    inv_state = fields.Selection([
        ('done', 'Green'),
        ('blocked', 'Red')], string='Facturas vencidas',
        copy=False, default='done',compute='_compute_inv')

    active_credit = fields.Boolean(
        string="Activar credito",
        related="partner_id.active_credit"
    )


    @api.depends('amount_total')
    def _compute_amount_cal(self):
        for rec in self:
            if rec.partner_id.active_credit == True:
                if self.partner_id.amount_limit == 0:
                    rec.limit_state = 'blocked'
                else:
                    if rec.amount_total > rec.amount_limit_total:
                        rec.limit_state = 'blocked'
                    else:
                        rec.limit_state = 'done'
            else:
                rec.limit_state = 'blocked'

    @api.depends('amount_total')
    def _compute_inv(self):
        for rec in self:            
            validate = rec.validate_invoice()
            print("++++++++++++",validate)
            if validate == True:
                rec.inv_state = 'blocked'
            else:
                
                rec.inv_state = 'done'

    def action_confirm(self):
        vals = super(SaleOrder, self).action_confirm()
        if self.partner_id.active_credit == True:
            if self.limit_state == 'blocked' or self.inv_state == 'blocked':
                self.state = 'locked'
                picking = self.env['stock.picking'].search([('origin','=',self.name),('state','!=','cancel')])
                if picking:
                    for p in picking:
                        p.write({'state':'locked'})
                amount_use = self.partner_id.amount_use
                amount_total = self.partner_id.amount_total
                print("+++amount_total+++++",amount_use,"+++amount_total+++++",amount_total)
                self.partner_id.write({'amount_total': amount_total - self.amount_total,'amount_use': amount_use + self.amount_total})
            else:
                amount_use = self.partner_id.amount_use
                amount_total = self.partner_id.amount_total
                print("+++amount_total+++++",amount_use,"+++amount_total+++++",amount_total)
                self.partner_id.write({'amount_total': amount_total - self.amount_total,'amount_use': amount_use + self.amount_total})

        return vals


    def action_confirm_lock(self):
        for rec in self:
            print("0000000000000")
            rec.write({'state':'sale'})
            picking = self.env['stock.picking'].search([('origin','=',rec.name),('state','=','locked')])
            if picking:
                for p in picking:
                    p.action_confirm_lock()


    def validate_invoice(self):
        for rec in self:
            if rec.amount_limit_total == 0:
                rec.amount_limit_total = rec.partner_id.amount_total
            print("--------",fields.Date.context_today(self),".........",rec.partner_id.property_payment_term_id.term_days)
            expired_date = fields.Datetime.from_string(fields.Date.context_today(self)) - relativedelta(days=rec.partner_id.property_payment_term_id.term_days)
            date_ex = fields.Datetime.to_string(fields.Datetime.context_timestamp(self, fields.Datetime.from_string(expired_date)))[:10]
            print("..........",date_ex)
            invoice = self.env['account.move'].search_count([('partner_id','=',rec.partner_id.id),('move_type','=','out_invoice'),('amount_residual','>',0),('invoice_date_due','<=',date_ex)])
            print("..........",invoice)
            if invoice > 0:
                return True
            else:
                return False


    def action_cancel(self):
        vals = super(SaleOrder, self).action_cancel()
        amount_use = self.partner_id.amount_use
        amount_total = self.partner_id.amount_total
        if amount_total > 0:
            print("+++amount_total+++++",amount_use,"+++amount_total+++++",amount_total)
            self.partner_id.write({'amount_total': amount_total - self.amount_total,'amount_use': amount_use - self.amount_total})
        else:
            print("+++amount_total+++++",amount_use,"+++amount_total+++++",amount_total)
            self.partner_id.write({'amount_total': amount_total + self.amount_total,'amount_use': amount_use - self.amount_total})
     
        return vals



