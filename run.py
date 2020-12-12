#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
run.py: App run of the GLOG Project.
"""

__author__ = "ALVES Marine, BOLTEAU Mathieu, CARRIAT Mélanie, CORNIER Alexandre, DRANCÉ Martin, JELIN Rémy and NEUHAUS Abdelghani"
__copyright__ = "Copyright (C) 2020, ALVES M., BOLTEAU M., CARRIAT M., CORNIER A., DRANCÉ M., JELIN R. and NEUHAUS A."
__license__ = " GNU General Public License v3"
__version__ = "1.0.0"

# Libraries imports
from app import app
import os

# This is needed for Heroku configuration as in Heroku our app will porbably not run on port 5000 as Heroku will automatically assign a port for our application.
port = int(os.environ.get("PORT", 5000))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)
