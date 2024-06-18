# -*- coding: utf-8 -*-
{
    'name': "Administración Académica",

    'summary': "Registro de alumnos, profesores, materias, cursos, inscripciones, calificaciones, mensualidades, comunicados, asistencias, horarios, sucursales, directores, administrativos, etc.",

    'description': """
    Long description of module's purpose
    """,

    'author': "Carlos Vargas",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Administración',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','web','hr','hr_attendance','website'],

    # always loaded

    'data': [
        'security/ir.model.access.csv',
        'security/groups.xml',
        'views/greet_dashboard.xml',
        'views/record_profesores.xml',
        'views/record_materia.xml',
        'views/record_carga_horaria.xml',
        'views/record_curso.xml',
        'views/record_apoderado.xml',
        'views/record_alumno.xml',
        'views/record_inscripcion.xml',
        'views/record_gestion.xml',
        'views/record_periodo.xml',
        'views/record_tipo_periodo.xml',
        'views/record_calificacion.xml',
        'views/record_mensualidad.xml',
        'views/record_costo_mensualidad.xml',
        'views/record_comunicados.xml',
        'views/record_detalle_comunicados.xml',
        'views/record_clase.xml',
        'views/record_asistencia.xml',
        'views/record_horario.xml',
        'views/record_horario_materia.xml',
        'views/record_materias_profesor.xml',
        'views/record_curso_materia.xml',
        'views/record_comunicado_prueba.xml',
        'views/record_sucursal.xml',
        'views/record_director.xml',
        'views/record_administrativo.xml',
        'views/record_profesor_sucursal_rel.xml',
        'views/menu_dashboard.xml',

        #'views/RRHH/record_alumno.xml',
        #'views/RRHH/menu_rrhh.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,  
    'assets':{
        'web.assets_backend':[
            'administracion_academica/static/src/components/**/*.js',
            'administracion_academica/static/src/components/**/*.xml',
        ],
    },
    #'qweb':['static/src/xml/dashboard.xml'],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

