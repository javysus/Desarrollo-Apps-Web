#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import cgi 
import json 

from db import DB

print("Content-type: text/html; charset=UTF-8")
print()
sys.stdout.reconfigure(encoding='utf-8')

db = DB('localhost', 'cc500241_u', 'salesPertj', 'cc500241_db')
form = cgi.FieldStorage()
id_comuna = form.getvalue('comuna')

results = db.getActComuna(int(id_comuna))
results_final = []
for actividad in results:
    id_act = actividad[0]
    fotos = db.getAllFotos(int(id_act))
    fila = list(actividad)
    fila.append(fotos)
    results_final.append(tuple(fila))


print(json.dumps(results_final,default=str))