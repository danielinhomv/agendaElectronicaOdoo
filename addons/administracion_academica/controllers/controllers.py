# -*- coding: utf-8 -*-
# from odoo import http


# class AdministracionAcademica(http.Controller):
#     @http.route('/administracion_academica/administracion_academica', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/administracion_academica/administracion_academica/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('administracion_academica.listing', {
#             'root': '/administracion_academica/administracion_academica',
#             'objects': http.request.env['administracion_academica.administracion_academica'].search([]),
#         })

#     @http.route('/administracion_academica/administracion_academica/objects/<model("administracion_academica.administracion_academica"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('administracion_academica.object', {
#             'object': obj
#         })

# class QwebTutorials(http.Controller):
#     @http.route('/qweb-tutorials', type="http", auth="public")
#     def qweb_tutorials(self):
#         """ QWEB tutorials"""
#         return http.request.render("qweb_tutorials.somePythonTemplate")