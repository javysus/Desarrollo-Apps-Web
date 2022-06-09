#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from db import DB

print("Content-type: text/html; charset=UTF-8")
print()
sys.stdout.reconfigure(encoding='utf-8')
db = DB('localhost', 'cc500241_u', 'salesPertj', 'cc500241_db')

regiones = db.getRegiones()
temas = db.getTemas()

options_regiones = "<option value=\"\" selected>Seleccione una región</option>"
options_temas = "<option value=\"\" selected>Seleccione un tema</option>"

for region in regiones:
    options_regiones += f"<option value={region[0]}>{region[1]}</option>"

for tema in temas:
    options_temas += f"<option value={tema[0]}>{tema[1]}</option>"

options_temas += "<option value=0>otro</option>"

options_comunas = "<option value=\"\" selected>Seleccione una comuna</option>"

with open('../informar_actividad.html','r', encoding='utf-8') as template:
    file = template.read()
    print(file.format(options_regiones,"", 
    options_comunas, "", 
    "","",
    "","",
    "","",
    "","",
    "","disabled",
    "","disabled",
    "","disabled",
    "","disabled",
    "","disabled",
    "","disabled",
    "","disabled",
    "",
    "","",
    "","",
    "",
    options_temas,"", "",
    ""))
