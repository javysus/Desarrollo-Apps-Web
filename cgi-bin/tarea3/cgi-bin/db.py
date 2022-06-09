#!/usr/bin/env python
import mysql.connector
import hashlib
import sys
import math
import json

def normalize(s):
    replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
    )
    for a, b in replacements:
        s = s.replace(a, b).replace(a.upper(), b.upper())
    return s


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

    def getActividadIndex(self, hash_foto):
        sql = f'''SELECT AC.id, CO.nombre, AC.sector, AC.nombre, AC.email, AC.celular, AC.dia_hora_inicio, AC.dia_hora_termino, AC.descripcion, TE.nombre, RE.nombre FROM foto FO, comuna CO, tema TE, region RE, actividad AC WHERE FO.ruta_archivo = '{hash_foto}' AND AC.comuna_id=CO.id AND AC.tema_id=TE.id AND CO.region_id = RE.id AND FO.actividad_id = AC.id;'''
        
        self.cursor.execute(sql)
        return self.cursor.fetchone()

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

    def getGrafDos(self):
        sql = '''SELECT TE.nombre, AC.tema_id, COUNT(AC.tema_id) AS n_acts FROM actividad AC INNER JOIN tema TE ON AC.tema_id = TE.id GROUP BY AC.tema_id;'''
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def getGrafTres(self):
        sql = '''SELECT MONTHNAME(dia_hora_inicio) AS mes,
        CASE WHEN HOUR(dia_hora_inicio) < 11 THEN 'mañana' 
        WHEN HOUR(dia_hora_inicio) >= 11 AND HOUR(dia_hora_inicio) < 15 THEN 'mediodia'
        ELSE 'tarde' END AS horario, COUNT(*) AS cantidad
        FROM actividad
        GROUP BY mes, horario
        ORDER BY MONTH(dia_hora_inicio);'''
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def getGrafUno(self):
        sql = '''SELECT thedays.theday, IFNULL(summary.`count`,0) `count`
   FROM (
        SELECT DATE(NOW())-INTERVAL seq.seq DAY theday   
          FROM (
                   SELECT 0 AS seq 
                     UNION ALL SELECT 1  UNION ALL SELECT 2 
                     UNION ALL SELECT 3  UNION ALL SELECT 4
                     UNION ALL SELECT 5  UNION ALL SELECT 6
              		UNION ALL SELECT 7  UNION ALL SELECT 8
              		UNION ALL SELECT 9 
                ) seq 
          ) thedays
   LEFT JOIN (
        SELECT DATE(act.dia_hora_inicio) theday,
               COUNT(*) `count`
          FROM actividad act
          WHERE act.dia_hora_inicio >= DATE(NOW()) - INTERVAL 9 DAY
         GROUP BY DATE(act.dia_hora_inicio)
       ) summary USING (theday)
   ORDER BY thedays.theday;'''
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    
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
            open(f"../../../media/{filename_hash}", "wb").write(fileobj.file.read()) # guarda el archivo localmente
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

    def getCantFotosComuna(self):
        sql = '''
        SELECT CO.nombre, COUNT(CO.nombre) AS fotos, CO.lat, CO.lng, CO.id FROM actividad AC INNER JOIN foto FO ON AC.id = FO.actividad_id LEFT JOIN comuna CO ON AC.comuna_id = CO.id GROUP BY CO.nombre ORDER BY fotos DESC;
        '''

        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def getActComuna(self, comuna):
        sql = f'''
        SELECT AC.id, AC.dia_hora_inicio, TE.nombre, AC.sector FROM actividad AC
        INNER JOIN tema TE ON AC.tema_id = TE.id WHERE AC.comuna_id = {comuna}'''

        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def insertLatLong(self):
        sql_alter = '''ALTER TABLE comuna ADD lng float, ADD lat float;'''

        self.cursor.execute(sql_alter)

        # Opening JSON file
        f = open('chile.json')
        data = json.load(f)
        for i in data:
            sql_update = f'''UPDATE comuna
            SET lng = {i['lng']}, lat = {i['lat']}
            WHERE nombre = \"{normalize(i['name'])}\";'''
            self.cursor.execute(sql_update)

        self.db.commit()
        f.close()
