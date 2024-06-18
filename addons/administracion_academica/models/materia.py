from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Materia(models.Model):
    _name = "administracion_academica.materia"
    _description = "Relacion de las materias del colegio"

    nombre = fields.Char(string="Nombre", required=True)
    
    asignacion_profesores = fields.One2many(
        "administracion_academica.carga_horaria_rel", 
        inverse_name="materia_id", 
        string="carga horaria")

    profesores = fields.Many2many(
        "administracion_academica.profesor", 
        compute="_compute_profesores", 
        string="Profesores")

    calificaciones = fields.One2many(
        'administracion_academica.calificacion', 
        inverse_name="materia_id",
        string="Materia")

    curso_materias = fields.One2many(
        "administracion_academica.curso_materia",
        inverse_name="materia_id",
        String="Cursos"
    )

    # cursos = fields.Many2many(
    #     "administracion_academica.curso",
    #     compute = "_compute_curso_materia",
    #     string= "Materias"
    # )

    cursos = fields.Many2many(
        "administracion_academica.curso",
        string ="Cursos",
        relation = "curso_materia",
        column1 = "materia_id",
        column2 = "curso_id"
    )
    
    asistencias = fields.One2many(
        'administracion_academica.clase',
        inverse_name ="materia_id",
        string = "Asistencias"
    )

    grado = fields.Selection(
        [
            ("primaria", "Primaria"),
            ("secundaria", "Secundaria"),
        ],
        string="Grado",
        default="primaria",
        required=True,
    )
    
    horarios_materia = fields.One2many(
        'administracion_academica.horario_materia', 
        'materia_id', 
        string='Horario de las clases',
        ondelete='cascade')    
    
    horarios = fields.Many2many(
        "administracion_academica.horario",
        string="Horario",
        relation = "horario_materia",
        column1 = "materia_id",
        column2 = "horario_id",
    )

    @api.depends("nombre")
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = (
                f"{rec.nombre}"
            )

    @api.depends('asignacion_profesores')
    def _compute_profesores(self):
        for materia in self:
            materia.profesores = materia.asignacion_profesores.mapped('profesor_id')

    @api.depends('cursos')
    def _compute_curso_materia(self):
        for materia in self:
            materia.cursos = materia.curso_materias.mapped('curso_id')

    @api.constrains('nombre', 'grado')
    def _check_unique_nombre_grado(self):
        for rec in self:
            existing = self.search([
                ('nombre', '=ilike', rec.nombre),
                ('grado', '=', rec.grado),
                ('id', '!=', rec.id)
            ])
            if existing:
                raise ValidationError("La materia con este nombre y grado ya existe.")

