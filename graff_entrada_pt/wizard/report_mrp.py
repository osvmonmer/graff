from odoo import fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo import models, fields, api, exceptions,_
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
from datetime import datetime
import json

class ReportMrp(models.TransientModel):
    _name = 'report.mrp'
    _description = 'Report  mrp'

    date_star = fields.Date(
        string="Fecha inicio",
        default=datetime.today()
    )
    date_end = fields.Date(
        string="Fecha Find",
        default=datetime.today()
    )

    def create_mrp_report(self):
        for rec in self:
            mrp_eli = self.env['reports.mrp'].search([('id','>',0)]).unlink()
            mrp = self.env['mrp.production'].search([('date_finished', '>=', rec.date_star),
                                                        ('date_finished', '<=', rec.date_end),
                                                        ('state', '<=', 'done')])

            datas = [] 
            if mrp:
                for m in mrp:
                    if m.producto_reporte_id:
                        print("xxxx sale", m.sale_id.name)
                        sale = self.env['sale.order.line'].search([('order_id', '=', m.sale_id.id),('product_id', '=', m.producto_reporte_id.id)],limit=1)
                        print("++++++++++++",sale.order_id.pricelist_id.currency_id.name)
                        tasa = 0
                        if sale.order_id.pricelist_id.currency_id.name == 'USD':
                            print("xx USD xxx",sale.order_id.date_order)
                            date = fields.Datetime.to_string(fields.Datetime.context_timestamp(self, fields.Datetime.from_string(sale.order_id.date_order)))[:10]
                            print("xxxxxxxxxxxxDATExxxxxxxxx",date)
                            tasa = 0
                            tcd = 0
                            pvmxd = 0
                            imported = 0
                            if sale.order_id.pricelist_id.currency_id.name == 'USD':
                                date = fields.Datetime.to_string(fields.Datetime.context_timestamp(self, fields.Datetime.from_string(sale.order_id.date_order)))[:10]
                                print("xxxxxxxxxxxxDATExxxxxxxxx",date)
                                tasas = self.env['res.currency.rate'].search([('name', '=', date),('currency_id', '=', sale.order_id.pricelist_id.currency_id.id)],limit=1)
                                if tasas:
                                    tcd = 1 / tasas.rate
                                    pvmxd = sale.price_unit * tcd
                                    imported = pvmxd * m.product_qty
                                    print("xxxx tasa xxxx", tasa , tasas.name)
                        datas.append({
                            'date': m.date_finished,
                            'cantidad': m.product_qty,
                            'no_client': m.res_partner_id.ref,
                            'clave': m.product_id.default_code,
                            'product_id': m.product_id.id,
                            'op_id': m.id,
                            'res_partner_id': m.res_partner_id.id,
                            'pesouni': m.product_id.weight,
                            'peso': m.product_id.weight * m.product_qty,
                            'estado': 'TERMINADO',
                            'pv': sale.price_unit if sale else 0,
                            
                            'currency_id': sale.order_id.pricelist_id.currency_id.id if sale.order_id.pricelist_id else False,
                            'tc': tcd if sale.order_id.pricelist_id.currency_id.name == 'USD' else 1,
                            'pvmx': pvmxd if sale.order_id.pricelist_id.currency_id.name == 'USD' else sale.price_unit,
                            'importe': imported if sale.order_id.pricelist_id.currency_id.name == 'USD' else sale.price_unit * m.product_qty,   
                            'date_star': rec.date_star,
                            'date_end': rec.date_end,

                        })
                    else:
                        print("xxxx sale", m.sale_id.name)
                        sale = self.env['sale.order.line'].search([('order_id', '=', m.sale_id.id),('product_id', '=', m.product_id.id)],limit=1)
                        print("++++++++++++",sale.order_id.pricelist_id.currency_id.name)
                        tasa = 0
                        tcd = 0
                        pvmxd = 0
                        imported = 0
                        if sale.order_id.pricelist_id.currency_id.name == 'USD':
                            date = fields.Datetime.to_string(fields.Datetime.context_timestamp(self, fields.Datetime.from_string(sale.order_id.date_order)))[:10]
                            print("xxxxxxxxxxxxDATExxxxxxxxx",date)
                            tasas = self.env['res.currency.rate'].search([('name', '=', date),('currency_id', '=', sale.order_id.pricelist_id.currency_id.id)],limit=1)
                            if tasas:
                                tcd = 1 / tasas.rate
                                pvmxd = sale.price_unit * tcd
                                imported = pvmxd * m.product_qty
                                print("xxxx tasa xxxx", tasa , tasas.name)
                            
                        datas.append({
                            'date': m.date_finished,
                            'cantidad': m.product_qty,
                            'no_client': m.res_partner_id.ref,
                            'clave': m.product_id.default_code,
                            'product_id': m.product_id.id,
                            'op_id': m.id,
                            'res_partner_id': m.res_partner_id.id,
                            'pesouni': m.product_id.weight,
                            'peso': m.product_id.weight * m.product_qty,
                            'estado': 'TERMINADO',
                            'pv': sale.price_unit if sale else 0,
                            'currency_id': sale.order_id.pricelist_id.currency_id.id if sale.order_id.pricelist_id else False,
                            'tc': tcd if sale.order_id.pricelist_id.currency_id.name == 'USD' else 1,
                            'pvmx': pvmxd if sale.order_id.pricelist_id.currency_id.name == 'USD' else sale.price_unit,
                            'importe': imported if sale.order_id.pricelist_id.currency_id.name == 'USD' else sale.price_unit * m.product_qty,     
                            'date_star': rec.date_star,
                            'date_end': rec.date_end,

                        })

            if datas:   
                report = self.env['reports.mrp'].create(datas)
                print(report)
                if report:
                    view_view_id = self.env.ref('graff_entrada_pt.reports_mrp_tree_view').id
                    return {
                        'type': 'ir.actions.act_window',
                        'res_model': 'reports.mrp',
                        'name': 'Entrada PT a Almacén',
                        'views': [(view_view_id, 'tree')],
			            'view_mode': 'tree',
                    }