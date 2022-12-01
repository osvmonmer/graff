# -*- coding: utf-8 -*-
from odoo import api, models, fields, tools, _
from odoo.tools.xml_utils import _check_with_xsd
from odoo.tools.float_utils import float_round, float_is_zero

import logging
import re
import base64
import json
import requests
import random
import string

from lxml import etree
from lxml.objectify import fromstring
from datetime import datetime
from io import BytesIO
from zeep import Client
from zeep.transports import Transport
from json.decoder import JSONDecodeError

class AccountMove(models.Model):
    _inherit = 'account.move'

    fields_sales = fields.Many2one('sale.order', string="Sale", compute="getValue",readonly=True)    

        
    def getValue(self):
        search = self.env['sale.order'].search([('name','=',self.invoice_origin)], limit = 1)
        if search:
            self.fields_sales = search.id
        else:
            factura = self.env['account.move'].search([('name','=',self.invoice_origin)], limit = 1)
            searchs = self.env['sale.order'].search([('name','=',factura.invoice_origin)], limit = 1)
            self.fields_sales = searchs.id

    @api.model
    def l10n_mx_edi_get_serie_and_folio(self):
        for rec in self:
            name_numbers = list(re.finditer('\d+', rec.name))
            serie_number = rec.name[:name_numbers[-1].start()]
            folio_number = name_numbers[-1].group().lstrip('0')
            print("+++++",serie_number,folio_number)
            return {
                'serie_number': serie_number,
                'folio_number': folio_number,
            }
