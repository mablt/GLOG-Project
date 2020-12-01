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
   prediction_figure = protein_data["2D_prediction"]
   encoded_prediction_figure = encode_2D_prediction_figure(prediction_figure)
   
#    figure_ramachandran = protein_data["ramachandran"]
   
   
   
   return render_template("index.html", protein=protein_data["pdb"], protein_id=id, 
                          protein_name=protein_data["name"], organism=protein_data["species"], 
                          protein_length=protein_data["length"], gene_name=protein_data["gene"],
                          figure_2D=encoded_prediction_figure)
 
 
@app.route('/<id>/blast', methods = ['POST', 'GET'])
def do_blast(id):
    return jsonify({"link1":"id1",
                   "link2":"id2",
                   "link3":"id3",})
   
@app.route('/<id>/ramachandran', methods = ['POST', 'GET'])
def do_ramachandran(id):
    ramachandran_figure = PROTEIN_REPOSITORY.make_ramachandran(id)
    encoded_ramachandran_figure = encode_ramachandran_figure(ramachandran_figure)
    return jsonify(encoded_ramachandran_figure)
   
   
def encode_2D_prediction_figure(prediction_figure):
   img = io.BytesIO()
   prediction_figure.savefig(img, format='png',
                bbox_inches='tight')
   img.seek(0)
   encoded = base64.b64encode(img.getvalue())
   return encoded.decode('utf-8')
   
def encode_ramachandran_figure(ramachandran_figure):
   ramachandran_figure.seek(0)
   encoded = base64.b64encode(ramachandran_figure.read())
   return encoded.decode('utf-8')