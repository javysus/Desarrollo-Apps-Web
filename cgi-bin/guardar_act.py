#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cgi
import os
import sys
import re
from db import DB

MAX_FILE_SIZE= 1000000
alerta_error = '<div class="alert alert-danger" role="alert">%s</div>'
#Validacion
def validarSector(sector):
    if len(sector)> 100:
        return alerta_error % "Ingrese un sector válido de largo máximo 100 caracteres"
    return ""

def validarNombre(nombre):
    regex = "^[a-zA-Z ]*$"

    if not(re.search(regex, nombre)) or len(nombre) > 200 or len(nombre) == 0:
        return alerta_error % "Ingrese un nombre válido de largo máximo 200 caracteres"
    return ""

#Revisar si esto valida si entra un emailo no
def validarEmail(email):
    regex = "^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$"

    if not(re.search(regex, email)):
        return alerta_error % "Ingrese un correo válido"
    return ""

def validarCelular(celular):
    regex = "^\+[1-9]\d{1,14}$"

    if not(re.search(regex, celular)):
        return alerta_error % "Ingrese un número de celular válido"
    else:
        return ""

def validarFecha(fecha):
    regex = "^([0-9]{4})-([0-1][0-9])-([0-3][0-9])\s([0-1][0-9]|[2][0-3]):([0-5][0-9])$"

    if not(re.search(regex, fecha) or len(fecha)>20):
        return alerta_error % "Ingrese una fecha válida"
    return ""

def validarOtrotema(tema):
    if len(tema) < 3 or len(tema) > 15:
        return "Ingrese un tema válido de mínimo 3 y máximo 15 caracteres<br>"
    return ""

def validarRedes(red, red_social):
    if len(red) < 4 or len(red) > 50:
        return f"Ingrese un link o ID de {red_social.capitalize()} válido de mínimo 4 y máximo 50 caracteres<br>"
    return ""

def validarFoto(foto, filename):
    tipo = foto.type
    size = os.fstat(foto.file.fileno()).st_size
    if tipo != 'image/png' and tipo != 'image/jpeg' and tipo != 'jpg':
        return f"Formato no válido de imagen para {filename}<br>"
    if size > MAX_FILE_SIZE:
        return f"El archivo {filename} es muy grande.<br>"
    return ""

print("Content-type: text/html; charset=UTF-8")
print()
sys.stdout.reconfigure(encoding='utf-8')
db = DB('localhost', 'cc500241_u', 'salesPertj', 'cc500241_db')

form = cgi.FieldStorage()
region = form.getvalue("region")
comuna = form.getvalue("comuna")
tema = form.getvalue("tema")
sector = form.getvalue("sector")
nombre = form.getvalue("nombre")
email = form.getvalue("email")
celular = form.getvalue("celular")
contactos = form.getlist("contactar-por")
fecha_inicio = form.getvalue("dia-hora-inicio")
fecha_termino = form.getvalue('dia-hora-termino')
descripcion = form.getvalue('descripcion-evento')

regiones = db.getRegiones()
temas = db.getTemas()

#Revisar datos de formulario
if not(region):
    options_regiones = "<option value=\"\" selected>Seleccione una región</option>"
    for region_db in regiones:
        options_regiones += f"<option value={region_db[0]}>{region_db[1]}</option>"
    options_comunas = "<option value=\"\" selected>Seleccione una comuna</option>"
else:
    options_regiones = "<option value=\"\">Seleccione una región</option>"
    for region_db in regiones:
        if(region_db[0] == int(region)):
            options_regiones += f"<option value={region_db[0]} selected>{region_db[1]}</option>"
        else:
            options_regiones += f"<option value={region_db[0]}>{region_db[1]}</option>"
    comunas = db.getComunas(region)
    if not(comuna):
        options_comunas = "<option value=\"\" selected>Seleccione una comuna</option>"
        for comuna_db in comunas:
            options_comunas+= f"<option value={comuna_db[0]}>{comuna_db[1]}</option>"
    else:
        options_comunas = "<option value=\"\" selected>Seleccione una comuna</option>"
        for comuna_db in comunas:
            if(comuna_db[0] == int(comuna)):
                options_comunas+= f"<option value={comuna_db[0]} selected>{comuna_db[1]}</option>"
            else:
                options_comunas+= f"<option value={comuna_db[0]}>{comuna_db[1]}</option>"

if not(tema):
    options_temas = "<option value=\"\" selected>Seleccione un tema</option>"
    for tema_db in temas:
        options_temas += f"<option value={tema_db[0]}>{tema_db[1]}</option>"
else:
    options_temas = "<option value=\"\">Seleccione un tema</option>"
    for tema_db in temas:
        if(tema_db[0] == int(tema)):
            options_temas += f"<option value={tema_db[0]} selected>{tema_db[1]}</option>"
        else:
            options_temas += f"<option value={tema_db[0]}>{tema_db[1]}</option>"

    if(tema=='0'):
        options_temas += "<option value=0 selected>otro</option>"
    else:
        options_temas += "<option value=0>otro</option>"


validacion = False
list_errores = []

#Validar que todo lo obligatorio haya sido subido: Region, comuna, nombre,email, fecha inicio, tema y foto


#Posicion 0: Region
if not(region):
    list_errores.append(alerta_error % "Seleccione una región")
else:
    list_errores.append("")

#Posicion 1: Comuna
if not(comuna):
    list_errores.append(alerta_error % "Seleccione una comuna")
else:
    list_errores.append("")

#Posicion 2: Sector 
if sector:
    sector_html = f"value=\'{sector}\'"
    list_errores.append(validarSector(sector))
else:
    sector_html = ""
    list_errores.append("")

#Posicion 3: Nombre 
if nombre:
    nombre_html = f"value=\'{nombre}\'"
    list_errores.append(validarNombre(nombre))
else:
    nombre_html = ""
    list_errores.append(alerta_error % "Ingrese un nombre")
#Posicion 4: Email 

if email:
    email_html = f"value=\'{email}\'"
    list_errores.append(validarEmail(email))
else: 
    email_html = ""
    list_errores.append(alerta_error % "Ingrese un correo")
#Posicion 5: Celular 

if (celular):
    celular_html = f"value=\'{celular}\'"
    list_errores.append(validarCelular(celular))
else:
    celular_html = ""
    list_errores.append("")

#Posicion 6: Contactos

error_contactos = ""
contactos_html = []
redes = {'whatsapp': ["","disabled"], 'telegram':["","disabled"], 'twitter': ["","disabled"], 'instagram':["","disabled"], 'facebook':["","disabled"], 'tiktok':["","disabled"], 'otra': ["","disabled"]}

if contactos != []:
    for contacto in contactos:
        redes[contacto][0] = "checked"
        contacto_link = form.getvalue(contacto+"-link")
        if (contacto_link):
            error_contactos += validarRedes(contacto_link, contacto)
            redes[contacto][1] = f"value=\'{contacto_link}\'"
        else:
            error_contactos += f"Ingrese un link para {contacto.capitalize()}<br>"

    if(error_contactos == ""):
        list_errores.append("")
    else:
        list_errores.append(alerta_error % error_contactos)

    for valor in redes.values():
        contactos_html.extend(valor)
else:
    list_errores.append("")
    contactos_html = ["","disabled",
    "","disabled",
    "","disabled",
    "","disabled",
    "","disabled",
    "","disabled",
    "","disabled"]


#Posicion 7: Fecha de inicio 

if not(fecha_inicio):
    fecha_inicio_html = ""
    list_errores.append(alerta_error % "Ingrese una fecha de inicio")
else:
    fecha_inicio_html = f"value=\'{fecha_inicio}\'"
    list_errores.append(validarFecha(fecha_inicio))

#Posicion 8: Fecha de termino 

if fecha_termino:
    fecha_termino_html = f"value=\'{fecha_termino}\'"
    list_errores.append(validarFecha(fecha_termino))
else:
    fecha_termino_html = ""
    list_errores.append("")

#Descripcion

if descripcion:
    descripcion_html = descripcion
else:
    descripcion_html = ""
#Posicion 9: Tema 
"""Tema
Casos: - No se selecciona un tema
- Se selecciona otro tema y no se escribe el tema correspondiente
- Se selecciona otro tema y no cumple con formato"""

agregarNuevoTema = False
otro_tema_html = ""
if not(tema):
    list_errores.append(alerta_error % "Seleccione un tema")
elif tema == '0':
    agregarNuevoTema = True
    #Validar otro tema
    otro_tema = form.getvalue("otro")
    if not(otro_tema):
        otro_tema_html='<label for="otro" class="col-sm-2 col-form-label">Descripción de otro tema </label><div class="col-sm-10"><input type="text" name="otro" id="otro" class="form-control"></div>'
        list_errores.append(alerta_error % "Ingrese un tema")
    
    else:
        otro_tema_html = f'<label for="otro" class="col-sm-2 col-form-label">Descripción de otro tema </label><div class="col-sm-10"><input type="text" name="otro" id="otro" class="form-control" value={otro_tema}></div>'
        list_errores.append(validarOtrotema(otro_tema))
else:
    list_errores.append("")


#Posicion 10: Fotos
error_fotos = ""
fotoMultiple = False
foto = form.getvalue('foto-actividad')
if isinstance(foto, list):
    fotoMultiple = True
    fotos_actividad = form['foto-actividad']
    largo = 0
    for foto in fotos_actividad:
        error_fotos += validarFoto(foto, foto.filename)
        largo += 1

    if(largo > 5):
        error_fotos += "Se ha superado el máximo de fotos<br>"
    if error_fotos == "":
        list_errores.append("")
    else:
        list_errores.append(alerta_error % error_fotos)
else:
    foto_actividad = form['foto-actividad']

    if(foto_actividad.filename):
        error = validarFoto(foto_actividad, foto_actividad.filename)
        if error=="":
            list_errores.append("")
        else:
            list_errores.append(alerta_error % error)
    else:
        list_errores.append(alerta_error % "Ingrese al menos una foto")

for valor in list_errores:
    if (valor != ""):
        validacion = True #Si hay algun error, hay que llevar a pagina de validacion

#redes_link = {'whatsapp': "", 'telegram': "", 'twitter': "", 'instagram': "", 'facebook': "", 'tiktok': "", 'otra': ""}
#redes_enabled = {'whatsapp': "disabled", 'telegram': "disabled", 'twitter': "disabled", 'instagram': "disabled", 'facebook': "disabled", 'tiktok': "disabled", 'otra': "disabled"}
if(validacion):
    with open('../informar_actividad.html','r', encoding='utf-8') as template:
        file = template.read()
        """valores = [region, comuna, sector, nombre, email, celular]

        if contactos != []:
            for contacto in contactos:
                contacto_link = form.getvalue(contacto+"-link")
                redes_link[contacto] = contacto_link
                redes_enabled[contacto] = ""

        for red in redes_link.keys():
            valores.append(redes_enabled[red])
            valores.append(redes_link[red])
            #file = file % (redes_enabled[red],redes_link[red])
        valores.extend([fecha_inicio, fecha_termino, descripcion, tema])
        print(valores)
        print(len(valores))
        file = file % tuple(valores)"""
        """Regiones, errores en region ,errores en comuna, errores en sector, errores en nombre, 5: errores en email, errores en celular, errores en redes, errores en fecha inicio
        errores en fehca de termino, 10: temas, errores en tema, errores en fotos
        print(file.format(options_regiones, list_errores[0],list_errores[1],list_errores[2],list_errores[3], list_errores[4],
        list_errores[5],list_errores[6],list_errores[7],list_errores[8], options_temas,list_errores[9], list_errores[10]))"""

        print(file.format(options_regiones, list_errores[0],
        options_comunas, list_errores[1],
        sector_html, list_errores[2],
        nombre_html, list_errores[3], 
        email_html, list_errores[4],
        celular_html, list_errores[5],
        contactos_html[0], contactos_html[1],
        contactos_html[2], contactos_html[3],
        contactos_html[4], contactos_html[5],
        contactos_html[6], contactos_html[7],
        contactos_html[8], contactos_html[9],
        contactos_html[10], contactos_html[11],
        contactos_html[12], contactos_html[13],
        list_errores[6],
        fecha_inicio_html, list_errores[7],
        fecha_termino_html, list_errores[8],
        descripcion_html,
        options_temas, otro_tema_html, list_errores[9], 
        list_errores[10]))

else:
    #Agregar nuevo tema a la base de datos
    if (agregarNuevoTema):
        id_tema = db.guardarTema(otro_tema)
        data = (comuna, sector, nombre, email, celular, fecha_inicio, fecha_termino, descripcion, id_tema)

    else:
        data = (comuna, sector, nombre, email, celular, fecha_inicio, fecha_termino, descripcion, tema)

    #Agregar actividad
    id_actividad = db.guardarActividad(data)

    #Agregar contactos
    for contacto in contactos:
        contacto_link = form.getvalue(contacto+"-link")
        db.guardarContactos((contacto, contacto_link, id_actividad))

    #Agregar imagenes
    if fotoMultiple:
        for foto in fotos_actividad:
            data = (id_actividad, foto)
            db.guardarFotos(data)
    else:
        data = (id_actividad, foto_actividad)
        db.guardarFotos(data)
    with open('../form_exitoso.html', 'r', encoding='utf-8') as template:
        file = template.read()
        print(file)