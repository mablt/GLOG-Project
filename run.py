#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from app import app
# ADJUSTMENT: import the library that will let us read environment variables
import os

# ADJUSTMENT: This is needed for Heroku configuration as in Heroku our
# app will porbably not run on port 5000 as Heroku will automatically
# assign a port for our application.
port = int(os.environ.get("PORT", 5000))

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=port, debug=True)