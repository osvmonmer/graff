from odoo import models, fields, api


class ResCompany(models.Model):
    _inherit = 'res.company'

    iconreport = fields.Binary(
        string="Imagen report fabricacion"
    )