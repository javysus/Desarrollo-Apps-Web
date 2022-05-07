# !/usr/bin/python3
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
id_region = form.getvalue('id_region')

results = db.getComunas(id_region)

print(json.dumps(results))