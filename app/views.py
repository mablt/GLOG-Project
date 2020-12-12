#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
views.py: Flask views of the GLOG Project.
"""

__author__ = "ALVES Marine, BOLTEAU Mathieu, CARRIAT Mélanie, CORNIER Alexandre, DRANCÉ Martin, JELIN Rémy and NEUHAUS Abdelghani"
__copyright__ = "Copyright (C) 2020, ALVES M., BOLTEAU M., CARRIAT M., CORNIER A., DRANCÉ M., JELIN R. and NEUHAUS A."
__license__ = " GNU General Public License v3"
__version__ = "1.0.0"

# Libraries imports
from app import app
from flask import render_template, request, jsonify

# Local imports
from .ProteinRepository import ProteinRepository

PROTEIN_REPOSITORY = ProteinRepository()

# Initial webpage
@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template("index.html")

# Show a protein
@app.route('/<id>', methods=['POST', 'GET'])
def get_protein(id):
    protein_data = PROTEIN_REPOSITORY.get_protein_informations_by_id(id)
    return jsonify(protein_data)

# Show the blast result of a protein
@app.route('/<id>/blast', methods=['POST', 'GET'])
def do_blast(id):
    blast_ids = PROTEIN_REPOSITORY.get_blast(id)
    return jsonify(blast_ids)

# Show the ramachandran result of a protein
@app.route('/<id>/ramachandran', methods=['POST', 'GET'])
def do_ramachandran(id):
    ramachandran_figure = PROTEIN_REPOSITORY.get_ramachandran(id)
    return jsonify(ramachandran_figure)
