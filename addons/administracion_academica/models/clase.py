from odoo import models, fields, api


class Clase(models.Model):
    _name = "administracion_academica.clase"
    _description = "clases del alumno"

    profesor_id = fields.Many2one(
        'administracion_academica.profesor', 
        string='Profesor',
        )
    
    curso_id = fields.Many2one('administracion_academica.curso', string='Curso')
    
    materia_id = fields.Many2one(
        'administracion_academica.materia', 
        string ="Materias asignadas",
        domain="[('id', 'in', materias_profesor)]")
    
    # horario_id = fields.Many2one('administracion_academica.', string='Schedule')
    asistencias = fields.One2many(
        'administracion_academica.asistencia', 
        'clase_id', 
        string='Asistencias',
        ondelete='cascade')

    alumnos = fields.Many2many(
        'administracion_academica.alumno',
        compute = "_compute_alumno",
        string = "Alumnos"
    )

    materias_profesor = fields.Many2many(
        'administracion_academica.materia', 
        string="Materias del Profesor", 
        compute="_compute_materias"
        )

    @api.depends('asistencias')
    def _compute_alumno(self):
        for clase in self:
            clase.alumnos = clase.asistencias.mapped('alumno_id')

    @api.depends("curso_id", "materia_id")
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = (
                f"{rec.curso_id.nombre}-{rec.materia_id.nombre}"
            )

    @api.model
    def create(self, vals):
        clase = super(Clase, self).create(vals)
        alumnos = clase.curso_id.alumnos
        for alumno in alumnos:
            self.env['administracion_academica.asistencia'].create({
                'clase_id': clase.id,
                'alumno_id': alumno.id,
            })
        return clase

    @api.depends('profesor_id')
    def _compute_materias(self):
        for clase in self:
            current_user = self.env.user
            if current_user and current_user.email:
                profesor = self.env['administracion_academica.profesor'].search([
                 ('correo_electronico', '=', current_user.email)
            ])
                clase.profesor_id = profesor.id
            else:
                clase.profesor_id = False

            if clase.profesor_id:
                profesor = clase.profesor_id
                materia_ids = profesor.materias.ids
                clase.materias_profesor = [(6, 0, materia_ids)]
            else:
                clase.materias_profesor = [(5,)] 

