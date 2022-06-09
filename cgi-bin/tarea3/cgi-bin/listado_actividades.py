#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cgi
from itertools import count
import sys
import math
#import filetype
from db import DB

print("Content-type: text/html; charset=UTF-8")
print()
sys.stdout.reconfigure(encoding='utf-8')
db = DB('localhost', 'cc500241_u', 'salesPertj', 'cc500241_db')

#count_activities = db.getActivitiesCount()[0]
firstFive = db.getFiveLastActivities()
#paginas = math.ceil(count_activities/5)
paginas = db.getTotalPaginas()
"""if(count_activities%5 == 0):
    paginas = count_activities/5
else:
    if count_activities > 5:
        paginas = count_activities/5 + 1
    else:
        paginas = 1"""

paginar = '<li class="page-item disabled" id="prev-class"><a class="page-link" href="#" id="prev">Anterior</a></li>'
paginar += '<li class="page-item active" id="activar-1"><a class="page-link" id="1" href="#">1</a></li>'
for i in range(1,paginas):
    paginar+= f'<li class="page-item" id="activar-{i+1}"><a class="page-link" id="{i+1}" href="#">{i+1}</a></li>'
paginar += '<li class="page-item" id="next-class"><a class="page-link" href="#" id="next">Siguiente</a></li>'

filas_html =""
i=0
for actividad in firstFive:

    fila = '<tr class="position-relative">'
    cantidad_fotos = db.getFotoCount(actividad[0])[0]

    comuna = actividad[1]
    sector = actividad[2]
    nombre = actividad[3]
    email = actividad[4]
    celular = actividad[5]
    fecha_inicio = actividad[6]
    fecha_termino = actividad[7]
    descripcion = actividad[8]
    tema = actividad[9]

    fila+= f'<th>{fecha_inicio}</th> <th>{fecha_termino}</th> <th>{comuna}</th> <th>{sector}</th> <th>{tema}</th> <th>{nombre}</th> <th>{cantidad_fotos}</th> <th><a href="#" id="act-{i}-pag-1" class="btn btn-primary btn-sm stretched-link">Ver más</a></th>'
    fila += '</tr>'

    filas_html += fila
    i+=1

with open('../listado_actividades.html','r', encoding='utf-8') as template:
    file = template.read()
    print(file.format(filas_html, paginar))

