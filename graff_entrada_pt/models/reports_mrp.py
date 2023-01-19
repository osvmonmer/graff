# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class ReportsMrp(models.Model):
    _name = 'reports.mrp'
    _description = 'Branch state'

    date = fields.Date(
        string="Fecha"
    )
    cantidad = fields.Char(
        string="Cantidad"
    )
    no_client = fields.Char(
        string="NO. cliente"
    )
    clave = fields.Char(
        string="Clave"
    )
    product_id = fields.Many2one(
        'product.product',
        string='Nombre del producto',
    )
    op_id = fields.Many2one(
        'mrp.production',
        string='Orden produccion',
    )
    res_partner_id = fields.Many2one(
        'res.partner',
        string='Cliente',
    )
    pesouni = fields.Float(
        string='P/U',
    )
    peso = fields.Float(
        string='Peso',
    )
    estado = fields.Char(
        string='Estado',
    )
    pv = fields.Float(
        string='P/V U',
    )
    importe = fields.Float(
        string='Importe',
    )

    date_star = fields.Date(
        string="Fecha inicio",
    )
    date_end = fields.Date(
        string="Fecha Find",
    )

    def date_start(self):
        date = False
        for rec in self:
            date = rec.date_star
        
        return date

    def date_ends(self):
        date = False
        for rec in self:
            date = rec.date_end
        
        return date
