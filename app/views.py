from app import app
from flask import render_template, request, jsonify
from .ProteinRepository import ProteinRepository

PROTEIN_REPOSITORY = ProteinRepository()

# Page initiale
@app.route('/', methods = ['POST', 'GET'])
def index():
   return render_template("index.html")

# Affichage d'une protéine
@app.route('/<id>', methods = ['POST', 'GET'])
def get_pdb(id):  # A renommer
	protein_data = PROTEIN_REPOSITORY.get_protein_informations_by_id(id)
	return jsonify(protein_data)
 
@app.route('/<id>/blast', methods = ['POST', 'GET'])
def do_blast(id):
    blast_ids = PROTEIN_REPOSITORY.make_blast(id)
    return jsonify(blast_ids)
   
@app.route('/<id>/ramachandran', methods = ['POST', 'GET'])
def do_ramachandran(id):
    ramachandran_figure = PROTEIN_REPOSITORY.make_ramachandran(id)
    return jsonify(ramachandran_figure)
   