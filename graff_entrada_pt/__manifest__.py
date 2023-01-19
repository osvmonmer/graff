# -*- coding: utf-8 -*-
{
    'name': "graff_entrada_pt",

    'summary': """
        """,

    'description': """
        
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",
    'category': 'Uncategorized',
    'version': '14.1',
    'depends': ['mrp'],
    'data': [
        'security/ir.model.access.csv',
        'views/reports_mrp.xml',
        'views/mrp_production.xml',
        'views/res_company.xml',
        'wizard/report_mrp.xml',
        'report/template_reports_mrp.xml',
    ],
}
