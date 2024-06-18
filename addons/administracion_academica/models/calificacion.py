from odoo import models, fields, api
from odoo.exceptions import ValidationError

class calificacion(models.Model):
    _name = "administracion_academica.calificacion"
    _description = "notas de los alumnos"

    descripcion = fields.Char("Descripción")
    nota = fields.Float("Nota", required=True)

    alumno_id = fields.Many2one(
        "administracion_academica.alumno",
        string="Alumno", 
        domain="[('id', 'in', alumnos_curso)]"
        )
    
    # relacion con profesor (muchos a uno)
    profesor_id = fields.Many2one(
        'administracion_academica.profesor',
        string ="Profesor")

    # relacion con materia (muchos a uno)
    materia_id = fields.Many2one(
        'administracion_academica.materia', 
        string ="Materias asignadas",
        domain="[('id', 'in', materias_profesor)]"
        )
    
     # relacion con curso (muchos a uno)
    curso_id = fields.Many2one(
        'administracion_academica.curso', 
        string ="Curso")
    
    # relacion con periodo (muchos a uno)
    periodo_id = fields.Many2one( 
        'administracion_academica.periodo', 
        string ="Periodo", 
        required= True)

    materias_profesor = fields.Many2many(
        'administracion_academica.materia', 
        string="Materias del Profesor", 
        compute="_compute_materias")
    
    alumnos_curso = fields.Many2many(
        'administracion_academica.alumno', 
        string="Alumnos del curso", 
        compute="_compute_alumnos")
    
    profesor_calificacion = fields.Many2one(
        'administracion_academica.profesor',
        string ="profesor calificacion"
    )

    @api.depends('alumno_id')
    def _compute_materias(self):
        for calificacion in self:
            user_id = self.env.uid
            if  user_id:
                carga_horaria_rel = self.env['administracion_academica.carga_horaria_rel'].search([
                    ('profesor_id.user_id', '=',  user_id)
                ])
                materias_ids = carga_horaria_rel.mapped('materia_id.id')
                calificacion.materias_profesor = [(6, 0, materias_ids)]
            else:
                calificacion.materias_profesor = [(5,)] 
                
    @api.onchange('materias_profesor')
    def _onchange_materias_del_profesor(self):
        if not self.materias_profesor:
            self.materia_id = False

    # Obtener los alumnos inscritos según el curso
    @api.depends('curso_id')
    def _compute_alumnos(self):
        for calificacion in self:
            if calificacion.curso_id:
                curso = calificacion.curso_id
                alumnos_ids = curso.alumnos.ids
                calificacion.alumnos_curso = [(6, 0, alumnos_ids)]
            else:
                calificacion.alumnos_curso = [(5,)] 

    @api.onchange('alumnos_curso')
    def _onchange_alumnos_curso(self):
        if not self.alumnos_curso:
            self.curso_id = False
            
    @api.constrains("nota")
    def _check_nota(self):
        for rec in self:
            # if not (0 <= rec.nota <= 100):
            #     raise ValidationError("La nota debe estar entre 0 y 100.")
            # Verificar que el valor de 'nota' es un número y está en el rango permitido
            if not isinstance(rec.nota, (int, float)) or not (0 <= rec.nota <= 100):
                raise ValidationError("La nota debe ser un número entre 0 y 100.")
            