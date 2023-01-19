from odoo import models, fields, api


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    res_partner_id = fields.Many2one(
        'res.partner',
        string='Cliente',
    )
    sale_id = fields.Many2one(
        'sale.order',
        string='Venta',
    )

    producto_reporte_id = fields.Many2one(
        'product.product', 'Product',
        domain="""[
            ('type', 'in', ['product', 'consu']),
            '|',
                ('company_id', '=', False),
                ('company_id', '=', company_id)
        ]
        """,
        check_company=True,
    )