from app import app
from flask import render_template, request
from .ProteinRepository import ProteinRepository
import io, base64


########################### LIKE SERVER2 BEFORE ###########################

PROTEIN_REPOSITORY = ProteinRepository()

# Page initiale
@app.route('/', methods = ['POST', 'GET'])
def index():
   return render_template("index.html")

# Affichage d'une protéine
@app.route('/<id>', methods = ['POST', 'GET'])
def get_pdb(id):  # A renommer
   protein = PROTEIN_REPOSITORY.get_protein_by_id(id)
   
   # Lines 24 to 37 : TO MODIFY !      # TODO
   pdb =  protein.get_pdb_file()
   protein_name = protein.get_name()
   organism = protein.get_species()
   protein_length = protein.get_length()
   gene_name = protein.get_gene()
   fig = protein.get_2D_prediction_figure()
   # Convert fig object to html
   img = io.BytesIO()
   fig.savefig(img, format='png',
                bbox_inches='tight')
   img.seek(0)
   encoded = base64.b64encode(img.getvalue())
   html_fig =  encoded.decode('utf-8')
   return render_template("index.html", protein = pdb, protein_id= id, 
                          protein_name=protein_name, organism=organism, 
                          protein_length=protein_length, gene_name=gene_name,
                          figure_2D=html_fig)
 

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