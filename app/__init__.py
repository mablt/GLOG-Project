from flask import Flask
import requests
import json

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

from app import views