from odoo import models, fields, api


# tabla intermedia entre materia y profesor
class Horario(models.Model):
    _name = "administracion_academica.horario"
    _description = "Horario de las materias"

    dia = fields.Selection([
        ('Lunes', 'Lunes'),
        ('Martes', 'Martes'),
        ('Miércoles', 'Miércoles'),
        ('Jueves', 'Jueves'),
        ('Viernes', 'Viernes'),
        ('Sábado', 'Sábado'),
    ],
    string =" Dia de la semana",
    required=True)

    hora_ini = fields.Float(string="Hora de inicio", required=True,digits=(2, 2))
    hora_final = fields.Float(string="Hora de fin", required=True,digits=(2, 2))

    horarios_materia = fields.One2many(
        'administracion_academica.horario_materia', 
        'horario_id', 
        string='Horario de las materias',
        ondelete='cascade')
    
    materias = fields.Many2many(
        "administracion_academica.materia",
        string ="Materias",
        relation = "horario_materia",
        column1 = "horario_id", 
        column2 = "materia_id" 
    )

    @api.depends("dia","hora_ini","hora_final")
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = (
                # f"{self.dia} : {rec.hora_ini} - {rec.hora_final}"
                f"{rec.dia} : {self._float_to_time(rec.hora_ini)} - {self._float_to_time(rec.hora_final)}"
            )

    def _float_to_time(self, float_time):
        hours = int(float_time)
        minutes = int((float_time - hours) * 60)
        return f"{hours:02d}:{minutes:02d}"
