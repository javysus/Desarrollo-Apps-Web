#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cgi
import os
import sys
import re
from db import DB

MAX_FILE_SIZE= 100000
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
    if tipo != 'image/png':
        return f"Formato no válido de imagen para {filename}<br>"
    if size > MAX_FILE_SIZE:
        return f"El archivo {filename} es muy grande.<br>"
    return ""

print("Content-type: text/html; charset=UTF-8")
print()
sys.stdout.reconfigure(encoding='utf-8')
db = DB('localhost', 'cc500241_u', 'salesPertj', 'cc500241_db')

regiones = db.getRegiones()
temas = db.getTemas()

options_regiones = ""
options_temas = ""

for region in regiones:
    options_regiones += f"<option value= {region[0]}>{region[1]}</option>"

for tema in temas:
    options_temas += f"<option value= {tema[0]}>{tema[1]}</option>"

options_temas += "<option value=0>otro</option>"

form = cgi.FieldStorage()
validacion = False
list_errores = []

#Validar que todo lo obligatorio haya sido subido: Region, comuna, nombre,email, fecha inicio, tema y foto
region = form.getvalue("region")
comuna = form.getvalue("comuna")

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
sector = form.getvalue("sector")
if sector != None:
    list_errores.append(validarSector(sector))
else:
    list_errores.append("")

#Posicion 3: Nombre
nombre = form.getvalue("nombre")
if nombre == None:
    list_errores.append(alerta_error % "Ingrese un nombre")
else:
    list_errores.append(validarNombre(nombre))

#Posicion 4: Email 
email = form.getvalue("email")
if email == None:
    list_errores.append(alerta_error % "Ingrese un correo")
else:
    list_errores.append(validarEmail(email))

#Posicion 5: Celular 
celular = form.getvalue("celular")
if (celular):
    list_errores.append(validarCelular(celular))
else:
    list_errores.append("")

#Posicion 6: Contactos
contactos = form.getlist("contactar-por")
error_contactos = ""
if contactos != []:
    for contacto in contactos:
        contacto_link = form.getvalue(contacto+"-link")
        if (contacto_link):
            error_contactos += validarRedes(contacto_link, contacto)
        else:
            error_contactos += f"Ingrese un link para {contacto.capitalize()}<br>"
    if(error_contactos == ""):
        list_errores.append("")
    else:
        list_errores.append(alerta_error % error_contactos)
else:
    list_errores.append("")


#Posicion 7: Fecha de inicio 
fecha_inicio = form.getvalue("dia-hora-inicio")
if not(fecha_inicio):
    list_errores.append(alerta_error % "Ingrese una fecha de inicio")
else:
    list_errores.append(validarFecha(fecha_inicio))

#Posicion 8: Fecha de termino 
fecha_termino = form.getvalue('dia-hora-termino')
if fecha_termino:
    list_errores.append(validarFecha(fecha_termino))
else:
    list_errores.append("")

#Descripcion
descripcion = form.getvalue('descripcion-evento')

#Posicion 9: Tema 
"""Tema
Casos: - No se selecciona un tema
- Se selecciona otro tema y no se escribe el tema correspondiente
- Se selecciona otro tema y no cumple con formato"""
tema = form.getvalue("tema")
agregarNuevoTema = False
if not(tema):
    list_errores.append(alerta_error % "Seleccione un tema")
elif tema == "0":
    agregarNuevoTema = True
    #Validar otro tema
    otro_tema = form.getvalue("otro")
    if not(otro_tema):
        list_errores.append(alerta_error % "Ingrese un tema")
    
    else:
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
        errores en fehca de termino, 10: temas, errores en tema, errores en fotos"""
        print(file.format(options_regiones, list_errores[0],list_errores[1],list_errores[2],list_errores[3], list_errores[4],
        list_errores[5],list_errores[6],list_errores[7],list_errores[8], options_temas,list_errores[9], list_errores[10]))

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
"""print("Validacion", validacion)
print(list_errores)
data = (comuna, sector, nombre, email, celular, fecha_inicio, fecha_termino, descripcion)
print(data)"""
#db.guardarActividad(data)
