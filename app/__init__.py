#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
__init__.py: App init of the GLOG Project.
"""

__author__ = "ALVES Marine, BOLTEAU Mathieu, CARRIAT Mélanie, CORNIER Alexandre, DRANCÉ Martin, JELIN Rémy and NEUHAUS Abdelghani"
__copyright__ = "Copyright (C) 2020, ALVES M., BOLTEAU M., CARRIAT M., CORNIER A., DRANCÉ M., JELIN R. and NEUHAUS A."
__license__ = " GNU General Public License v3"
__version__ = "1.0.0"

# Libraries imports
from flask import Flask
import requests

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False   # For return jsonify in flask template

from app import views