# -*- coding: utf-8 -*-
# from odoo import http


# class WebsiteSlidesUpdate(http.Controller):
#     @http.route('/website_slides_update/website_slides_update/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/website_slides_update/website_slides_update/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('website_slides_update.listing', {
#             'root': '/website_slides_update/website_slides_update',
#             'objects': http.request.env['website_slides_update.website_slides_update'].search([]),
#         })

#     @http.route('/website_slides_update/website_slides_update/objects/<model("website_slides_update.website_slides_update"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('website_slides_update.object', {
#             'object': obj
#         })
