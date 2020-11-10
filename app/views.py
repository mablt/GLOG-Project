from app import app
from flask import render_template, request
from .models import print_pdb



########################### LIKE SERVER2 BEFORE ###########################

@app.route('/', methods = ['POST', 'GET'])
def index():
   return render_template("index.html")

@app.route('/result', methods = ['POST', 'GET'])
def get_pdb():
   if request.method == "POST":
      # protein = print_pdb(request.form["nm"])
      protein = getResponse(request.form["nm"])
      return render_template("printmolecule.html", protein = protein)
 

########################### LIKE SERVER1 BEFORE ###########################


"""
@app.route('/', methods = ['POST', 'GET'])
def index():
   return render_template("hello.html")

@app.route('/result', methods = ['POST', 'GET'])
def get_pdb():
   if request.method == "POST":
      protein = print_pdb(request.form["nm"])
      return render_template("result.html", protein = protein)

"""