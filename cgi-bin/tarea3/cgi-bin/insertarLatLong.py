#!/usr/bin/env python
# -*- coding: utf-8 -*-
from db import DB
db = DB('localhost', 'cc500241_u', 'salesPertj', 'cc500241_db')

db.insertLatLong()
print("Agregado latitud y longitud")