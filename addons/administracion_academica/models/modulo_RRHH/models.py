# from odoo import models, fields

# class AcademicAttendance(models.Model):
#     _inherit = 'hr.attendance'

#     academic_role = fields.Selection([
#         ('alumno', 'Alumno'),
#         ('profesor', 'Profesor'),
#         ('administrativo', 'Administrativo')
#     ], string='Roles')

# # Otros modelos de tu módulo
# class Alumno(models.Model):
#     _name = 'academic.student'
#     _inherits = {'hr.employee': 'employee_id'}

#     employee_id = fields.Many2one('hr.employee', required=True, ondelete='cascade')
#     student_number = fields.Char(string='Student Number', required=True)
#     # Otros campos específicos de estudiantes

# class Teacher(models.Model):
#     _name = 'academic.teacher'
#     _inherits = {'hr.employee': 'employee_id'}

#     employee_id = fields.Many2one('hr.employee', required=True, ondelete='cascade')
#     teacher_number = fields.Char(string='Teacher Number', required=True)
#     # Otros campos específicos de profesores

# class Staff(models.Model):
#     _name = 'academic.staff'
#     _inherits = {'hr.employee': 'employee_id'}

#     employee_id = fields.Many2one('hr.employee', required=True, ondelete='cascade')
#     staff_number = fields.Char(string='Staff Number', required=True)
#     # Otros campos específicos de personal administrativo
