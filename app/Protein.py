#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Protein.py: Protein class of the GLOG Project.

DESCRITPION #TODO
"""

__author__ = "ALVES Marine, BOLTEAU Mathieu, CARRIAT Mélanie, CORNIER Alexandre, DRANCÉ Martin, JELIN Rémy and NEUHAUS Abdelghani"
__copyright__ = "Copyright ?? December 2020"  # TODO
__version__ = "1.0.0"

# Libraries imports
import requests
import json
from xml.etree import ElementTree as ETree
from RamachanDraw import phi_psi, plot
import tempfile
import io
import base64
from pypdb import Query


# Local imports
from .ProteinPlotter import ProteinPlotter
from .PDBHandler import PDBHandler


class Protein():
    def __init__(self, id):
        self.m_id = id
        self.import_pdb_file_content()
        self.make_2D_prediction()
        self.blast_ids = self.ramachandran_figure = None
        self.import_xml_data_from_uniprot()

    def import_pdb_file_content(self):
        """
        Import the data (as string) from the pdb file of the protein and put it to 'pdb_content' variable
        """
        with open("./app/pdb/"+self.m_id+".pdb", 'r') as pdb_file_object:
            self.pdb_content = pdb_file_object.read()

    def make_2D_prediction(self):
        """
        Make the 2D prediction and put the matplotlib figure object in 'prediction_figure' variable
        """
        load = PDBHandler(self.m_id, "./app/pdb/")
        data, length = load.data_creation()
        model = ProteinPlotter(data, length)
        figure = model.draw_2D_protein()
        encoded_prediction_figure = self.encode_2D_prediction_figure(figure)
        self.prediction_figure = encoded_prediction_figure

    def import_xml_data_from_uniprot(self):
        path = "{http://uniprot.org/uniprot}"
        response = requests.get(
            "https://www.uniprot.org/uniprot/{}.xml".format(self.m_id))
        self.xml = ETree.fromstring(response.content)
        self.m_name = self.xml.find(
            "{}entry/{}protein/{}recommendedName/{}fullName".format(path, path, path, path)).text
        self.gene = self.xml.find(
            "{}entry/{}gene/{}name".format(path, path, path))
        if self.gene is None:
            self.gene = "N.A."
        else:
            self.gene = self.gene.text
        self.m_species = self.xml.find(
            "{}entry/{}organism/{}name".format(path, path, path)).text
        self.m_seq = self.xml.find(
            "{}entry/{}sequence".format(path, path)).text
        self.m_length = self.xml.find(
            "{}entry/{}sequence".format(path, path)).attrib['length']

    def make_ramachandran(self):
        path = "./app/pdb/"+self.m_id+".pdb"
        data = phi_psi(path)  # ramachadran data
        figure = tempfile.TemporaryFile()
        plot(path, out=figure)
        self.ramachandran_figure = self.encode_ramachandran_figure(figure)

    def make_blast(self):
        query = Query(self.m_seq, query_type="sequence",
                      return_type="polymer_entity")
        search = query.search()
        self.blast_ids = list()
        for i in range(3):
            long_id = search["result_set"][i]["identifier"]
            id = long_id.split('_')[0]   # Remove '_1' at the end of the ID
            self.blast_ids.append(id)
            
    def encode_2D_prediction_figure(self, prediction_figure):
        img = io.BytesIO()
        prediction_figure.savefig(img, format='png', bbox_inches='tight')
        img.seek(0)
        encoded = base64.b64encode(img.getvalue())
        return encoded.decode('utf-8')

    def encode_ramachandran_figure(self, ramachandran_figure):
        ramachandran_figure.seek(0)
        encoded = base64.b64encode(ramachandran_figure.read())
        return encoded.decode('utf-8')

    def get_pdb(self):
        return self.pdb_content

    def get_id(self):
        return self.m_id

    def get_name(self):
        return self.m_name

    def get_length(self):
        return self.m_length

    def get_seq(self):
        return self.m_seq

    def get_species(self):
        return self.m_species

    def get_gene(self):
        return self.gene

    def get_2D_prediction_figure(self):
        return self.prediction_figure

    def get_blast_ids(self):
        return self.blast_ids

    def get_ramachandran_figure(self):
        return self.ramachandran_figure

