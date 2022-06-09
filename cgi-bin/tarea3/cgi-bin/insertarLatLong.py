#!/usr/bin/env python
# -*- coding: utf-8 -*-
from db import DB
import sys
db = DB('localhost', 'cc500241_u', 'salesPertj', 'cc500241_db')
print("Content-type: text/html; charset=UTF-8")
print()
sys.stdout.reconfigure(encoding='utf-8')
db.insertLatLong()
print("Agregado latitud y longitud")