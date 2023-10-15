# -*- coding: utf-8 -*-
# from odoo import http


# class SalePricelistExtension(http.Controller):
#     @http.route('/sale_pricelist_extension/sale_pricelist_extension', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sale_pricelist_extension/sale_pricelist_extension/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('sale_pricelist_extension.listing', {
#             'root': '/sale_pricelist_extension/sale_pricelist_extension',
#             'objects': http.request.env['sale_pricelist_extension.sale_pricelist_extension'].search([]),
#         })

#     @http.route('/sale_pricelist_extension/sale_pricelist_extension/objects/<model("sale_pricelist_extension.sale_pricelist_extension"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sale_pricelist_extension.object', {
#             'object': obj
#         })
