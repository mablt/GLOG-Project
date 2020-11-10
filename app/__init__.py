from flask import Flask
import requests
import json

app = Flask(__name__)

from app import views