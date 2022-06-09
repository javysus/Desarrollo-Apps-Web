#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import json 

from db import DB

print("Content-type: text/html; charset=UTF-8")
print()
sys.stdout.reconfigure(encoding='utf-8')

db = DB('localhost', 'cc500241_u', 'salesPertj', 'cc500241_db')

results = db.getCantFotosComuna()
results_final = []
for comuna in results:
    id_comuna = comuna[4]
    results_2 = db.getActComuna(int(id_comuna))
    actividades = []
    for actividad in results_2:
        id_act = actividad[0]
        fotos = db.getAllFotos(int(id_act))
        fila = list(actividad)
        fila.append(fotos)
        actividades.append(tuple(fila))
    
    fila_comuna = list(comuna)
    fila_comuna.append(actividades)
    results_final.append(tuple(fila_comuna))
print(json.dumps(results_final, default=str))