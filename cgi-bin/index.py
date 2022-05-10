# -*- coding: utf-8 -*-
import cgi
import os
import sys
import re
#import filetype
from db import DB

print("Content-type: text/html; charset=UTF-8")
print()
sys.stdout.reconfigure(encoding='utf-8')
db = DB('localhost', 'cc500241_u', 'salesPertj', 'cc500241_db')

actividades = db.getFiveLastActivities()

filas_html = ""

for actividad in actividades:
    foto = db.getOneFoto(actividad[0])[0]
    fila = "<tr>"
    foto_hash = foto[1]
    foto_nombre = foto[2]

    comuna = actividad[1]
    sector = actividad[2]
    nombre = actividad[3]
    email = actividad[4]
    celular = actividad[5]
    fecha_inicio = actividad[6]
    fecha_termino = actividad[7]
    descripcion = actividad[8]
    tema = actividad[9]

    fila += f'<th>{fecha_inicio}</th> <th>{fecha_termino}</th> <th>{comuna}</th> <th>{sector}</th> <th>{tema}</th> <th> <img src="/media/{foto_hash}" class="rounded img-mini" alt="{foto_nombre}"></th>'

    fila += "</tr>"

    filas_html += fila

with open('../index.html','r', encoding='utf-8') as template:
    file = template.read()
    print(file.format(filas_html))


    