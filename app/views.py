from app import app
from flask import render_template, request, jsonify
from .ProteinRepository import ProteinRepository
import io, base64

PROTEIN_REPOSITORY = ProteinRepository()

# Page initiale
@app.route('/', methods = ['POST', 'GET'])
def index():
   return render_template("index.html")

# Affichage d'une protéine
@app.route('/<id>', methods = ['POST', 'GET'])
def get_pdb(id):  # A renommer
   protein_data = PROTEIN_REPOSITORY.get_protein_informations_by_id(id)
   # Convert fig object to html
   figure_2D_prediction = protein_data["2D_prediction"]
   img = io.BytesIO()
   figure_2D_prediction.savefig(img, format='png',
                bbox_inches='tight')
   img.seek(0)
   encoded = base64.b64encode(img.getvalue())
   html_figure_2D_prediction =  encoded.decode('utf-8')
   return render_template("index.html", protein=protein_data["pdb"], protein_id=id, 
                          protein_name=protein_data["name"], organism=protein_data["species"], 
                          protein_length=protein_data["length"], gene_name=protein_data["gene"],
                          figure_2D=html_figure_2D_prediction)
 
 
@app.route('/<id>/blast', methods = ['POST', 'GET'])
def do_blast(id):
   return jsonify({"link1":"id1",
                   "link2":"id2",
                   "link3":"id3",})