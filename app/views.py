from app import app
from flask import render_template, request
from .models import print_pdb


@app.route('/', methods = ['POST', 'GET'])
def index():
   return render_template("hello.html")

@app.route('/result', methods = ['POST', 'GET'])
def get_pdb():
   if request.method == "POST":
      protein = print_pdb(request.form["nm"])
      return render_template("result.html", protein = protein)