# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AddRateAddressDeliverys(models.Model):
    _inherit = 'res.partner'

    gln = fields.Char( string = 'GLN' )
    number_provideer = fields.Char(string='Provider number')
    number_sucursal = fields.Char( string="Branch number" )