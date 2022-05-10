#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cgi
import sys
import json
from db import DB

print("Content-type: text/html; charset=UTF-8")
print()
sys.stdout.reconfigure(encoding='utf-8')
db = DB('localhost', 'cc500241_u', 'salesPertj', 'cc500241_db')
form = cgi.FieldStorage()
pagina = form.getvalue('pagina')

actividades = db.getActivitiesPagination(int(pagina))
results = []
for actividad in actividades:
    cantidad_fotos = db.getFotoCount(actividad[0])[0]
    fila = list(actividad)
    fila.append(cantidad_fotos)
    results.append(tuple(fila))
results.append(db.getTotalPaginas())
print(json.dumps(results,default=str))