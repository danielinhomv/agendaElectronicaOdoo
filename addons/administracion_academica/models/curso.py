from odoo import models, fields, api
from odoo.exceptions import ValidationError


class curso(models.Model):
    _name = "administracion_academica.curso"
    _description = "Relacion de los cursos del colegio"

    nombre = fields.Char(string="Nombre del curso")
    # un curso tiene muchas calificaciones (uno a muchos)
    calificaciones = fields.One2many(
        'administracion_academica.calificacion', 
        inverse_name="curso_id",
        string="Curso")
    #relacion uno a muchos con inscripcion (uno a muchos)   
    inscripciones = fields.One2many(
        "administracion_academica.inscripcion", 
        inverse_name="curso_id", 
        string="Inscripciones")
    # relacion muchos con alumnos (muchos a muchos)
    alumnos = fields.Many2many(
        "administracion_academica.alumno", 
        compute="_compute_alumnos", 
        string="Alumnos")
    # relacion muchos con comunicados (uno a muchos)
    comunicados = fields.Many2many(
        "administracion_academica.comunicado_prueba",
        string="Comunicados",
        relation="comunicado_prueba_curso_rel",
        column1="curso_id",
        column2="comunicado_prueba_id",
        readonly=True
    )
    
    asistencias = fields.One2many(
        'administracion_academica.clase',
        inverse_name ="curso_id",
        string = "Asistencias"
    )

    horarios = fields.One2many(
        'administracion_academica.horario_materia',
        inverse_name = "curso_id",
        string = "horarios"
    )

    mensualidades = fields.One2many(
        "administracion_academica.mensualidad",
        inverse_name ="curso_id",
        string ="Mensualidades"
    )
    comunicados = fields.Many2many(
        "administracion_academica.comunicado_prueba",
        string="Comunicados",
        relation="comunicado_prueba_curso_rel",
        column1="curso_id",
        column2="comunicado_prueba_id",
        readonly=True
    )

    cursos_materia = fields.One2many(
        "administracion_academica.curso_materia",
        inverse_name = "curso_id",
        string = "Cursos"
    )

    materias = fields.Many2many(
        "administracion_academica.materia",
        string ="Cursos",
        relation = "curso_materia",
        column1 = "curso_id",
        column2 = "materia_id"
    )
    @api.depends("nombre")
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = (
                f"{rec.nombre}"
            )

    @api.depends('inscripciones')
    def _compute_alumnos(self):
        for curso in self:
            curso.alumnos = curso.inscripciones.mapped('alumno_id')


    # @api.depends('materias')
    # def _compute_curso_materia(self):
    #     for curso in self:
    #         curso.materias = curso.curso_materias.mapped('materia_id')
    
    @api.constrains('nombre')
    def _check_unique_nombre(self):
        for rec in self:
            existing = self.search([
                ('nombre', '=ilike', rec.nombre),
                ('id', '!=', rec.id)
            ])
            if existing:
                raise ValidationError("El curso con este nombre ya existe.")