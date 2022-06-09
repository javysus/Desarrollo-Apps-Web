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

graf_uno = db.getGrafUno()
graf_dos = db.getGrafDos()
graf_tres = db.getGrafTres()

#Formato de entrega de datos
#Grafico 1
fechas = []
act_por_fecha = []
for fila in graf_uno:
    fechas.append(fila[0])
    act_por_fecha.append(fila[1])

results_grafuno= [fechas, act_por_fecha]
#Grafico 2
temas = []
act_por_tema = []

for fila in graf_dos:
    temas.append(fila[0])
    act_por_tema.append(fila[2])

results_grafdos = [temas, act_por_tema]
#Grafico 3
datos = {'January': [0,0,0], 'February': [0,0,0], 'March': [0,0,0], 'April': [0,0,0], 'May': [0,0,0],
'June': [0,0,0], 'July': [0,0,0], 'August': [0,0,0], 'September': [0,0,0], 'October': [0,0,0], 'November': [0,0,0], 'December': [0,0,0]}
meses = list(datos.keys())

for fila in graf_tres:
    if(fila[1] == 'mañana'):
        datos[fila[0]][0] = fila[2]
    elif(fila[1] == 'mediodia'):
        datos[fila[0]][1] = fila[2]
    else:
        datos[fila[0]][2] = fila[2]

mañanas = []
mediodias = []
tardes = []
for dato in datos.values():
    mañanas.append(dato[0])
    mediodias.append(dato[1])
    tardes.append(dato[2])

results_graftres = [meses, mañanas, mediodias, tardes]

results = []
results.append(results_grafuno)
results.append(results_grafdos)
results.append(results_graftres)

#print(results)

print(json.dumps(results, default=str))