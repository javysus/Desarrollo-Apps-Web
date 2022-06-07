#!/usr/bin/env python
import mysql.connector
import hashlib
import sys
import math

class DB:
    def __init__(self, host, user, password, database):
        self.db = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.db.cursor()

    def getRegiones(self):
        sql = '''
            SELECT id, nombre
            FROM region
            '''
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def getComunas(self, region_id):
        sql = f'''
            SELECT id, nombre
            FROM comuna
            WHERE region_id = {region_id}
            '''
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def getTemas(self):
        sql = '''
            SELECT id, nombre
            FROM tema
            '''
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def getFiveLastActivities(self):
        sql = '''
            SELECT AC.id, CO.nombre, AC.sector, AC.nombre, AC.email, AC.celular, AC.dia_hora_inicio, AC.dia_hora_termino, AC.descripcion, TE.nombre 
            FROM actividad AC, comuna CO, tema TE WHERE AC.comuna_id=CO.id AND AC.tema_id=TE.id ORDER BY id DESC LIMIT 5
            '''
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def getActivitiesCount(self):
        sql = "SELECT COUNT(id) FROM actividad"
        self.cursor.execute(sql)
        return self.cursor.fetchone()

    def getActivitiesPagination(self, pag):
        offset = (pag-1)*5
        sql = f'''SELECT AC.id, CO.nombre, AC.sector, AC.nombre, AC.email, AC.celular, AC.dia_hora_inicio, AC.dia_hora_termino, AC.descripcion, TE.nombre 
            FROM actividad AC, comuna CO, tema TE WHERE AC.comuna_id=CO.id AND AC.tema_id=TE.id ORDER BY id DESC LIMIT 5 OFFSET {offset}'''
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def getActividad(self, pag, ind):
        offset = (pag-1)*5
        sql = f'''SELECT AC.id, CO.nombre, AC.sector, AC.nombre, AC.email, AC.celular, AC.dia_hora_inicio, AC.dia_hora_termino, AC.descripcion, TE.nombre,
            RE.nombre 
            FROM actividad AC, comuna CO, tema TE, region RE WHERE AC.comuna_id=CO.id AND AC.tema_id=TE.id AND CO.region_id = RE.id ORDER BY id DESC LIMIT 5 OFFSET {offset}'''
        self.cursor.execute(sql)
        return self.cursor.fetchall()[ind]

    def getFotoCount(self, id_act):
        sql = f"SELECT COUNT(id) FROM foto WHERE actividad_id={id_act}"
        self.cursor.execute(sql)
        return self.cursor.fetchone()

    def getOneFoto(self, id_act):
        sql = f'''
            SELECT id, ruta_archivo, nombre_archivo, actividad_id FROM foto WHERE actividad_id={id_act} ORDER BY id ASC LIMIT 1
            '''
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def getAllFotos(self, id_act):
        sql = f'''
            SELECT id, ruta_archivo, nombre_archivo, actividad_id FROM foto WHERE actividad_id={id_act} ORDER BY id ASC
            '''
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def getContactos(self, id_act):
        sql = f'''
            SELECT id, nombre, identificador, actividad_id FROM contactar_por WHERE actividad_id={id_act}
            '''
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def getTotalPaginas(self):
        count_activities = self.getActivitiesCount()[0]
        paginas = math.ceil(count_activities/5)

        return paginas

    def guardarTema(self, tema):
        sql =f'''
            INSERT INTO tema (nombre) 
            VALUES ('{tema}')
        '''
        self.cursor.execute(sql) # ejecuto la consulta
        self.db.commit() # modifico la base de datos

        return(self.cursor.lastrowid)
    def guardarActividad(self, data):
        sql ='''
            INSERT INTO actividad (comuna_id, sector, nombre, email, celular, dia_hora_inicio, dia_hora_termino, descripcion, tema_id) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
        self.cursor.execute(sql, data) # ejecuto la consulta
        self.db.commit() # modifico la base de datos

        return(self.cursor.lastrowid)

    def guardarFotos(self, data):

        # Procesar archivo

        fileobj = data[1]
        filename = fileobj.filename
        
        sql = "SELECT COUNT(id) FROM foto" # Cuenta los archivos que hay en la base de datos
        self.cursor.execute(sql)
        total = self.cursor.fetchall()[0][0] + 1
        filename_hash = hashlib.sha256(filename.encode()).hexdigest()[0:30] # aplica función de hash
        filename_hash += f"_{total}" # concatena la función de hash con el número total de archivos, nombre único
        # OJO: lo anterior puede ser peligroso en el caso en que se tenga un servidor que ejecute peticiones en paralelo.
        #       Lo que se conoce como un datarace

        # Guardar archivo
        try:
            open(f"../media/{filename_hash}", "wb").write(fileobj.file.read()) # guarda el archivo localmente
            sql_file = '''
            INSERT INTO foto (ruta_archivo, nombre_archivo, actividad_id) VALUES (%s, %s, %s)
        '''
            self.cursor.execute(sql_file, (filename_hash, filename, data[0]))  # ejecuta la query que guarda el archivo en base de datos
            self.db.commit() # modifico la base de datos

        except:
            print("ERROR AL GUARDAR EN LA BASE DE DATOS")
            sys.exit()

    def guardarContactos(self, data):
        sql ='''
            INSERT INTO contactar_por (nombre, identificador, actividad_id) VALUES (%s, %s, %s)
        '''
        self.cursor.execute(sql, data) # ejecuto la consulta
        self.db.commit() # modifico la base de datos
