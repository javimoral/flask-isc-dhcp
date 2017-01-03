#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tzlocal
import os
from flask import Flask
from flask_pymongo import PyMongo
from .jinja_filters import *

app = Flask(__name__)

# Load config
app.config['DEBUG'] = False if os.environ.get('DEBUG', 'False') == 'False' else True
app.config['LEASES_FILE'] = os.environ.get('LEASES_FILE')
app.config['TIMEZONE'] = str(tzlocal.get_localzone())

mongo = PyMongo(app)

if app.config['LEASES_FILE'] is None:
    print("Leases file must be defined")
    exit(-1)

import leases.controllers

# Jinja2 custom filters
app.jinja_env.filters['tolocaltime'] = tolocaltime
app.jinja_env.filters['datetimeformat'] = datetimeformat
app.jinja_env.filters['secstotimedelta'] = secstotimedelta
