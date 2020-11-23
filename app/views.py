from app import app
from flask import render_template, request
from .models import getResponse
from .Protein import *



########################### LIKE SERVER2 BEFORE ###########################

# Page initiale
@app.route('/', methods = ['POST', 'GET'])
def index():
   return render_template("index.html")

# Affichage d'une protéine
@app.route('/<id>', methods = ['POST', 'GET'])
def get_pdb(id):
   # if request.method == "POST":
      # protein = print_pdb(request.form["nm"])
      
   protein = Protein(id)
   protein.execute()
   pdb =  protein.get_pdb_file()
   protein_name = protein.get_name()
   organism = "..."
   protein_length = protein.get_length()
   gene_name = "..."
   
   # data = getResponse(id)
   return render_template("index.html", protein = pdb, protein_id= id, 
                          protein_name=protein_name, organism=organism, 
                          protein_length=protein_length, gene_name=gene_name)
 

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