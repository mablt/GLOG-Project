#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Protein.py: Protein class of the GLOG Project.

DESCRITPION #TODO
"""

__author__ = "ALVES Marine, BOLTEAU Mathieu, CARRIAT Mélanie, CORNIER Alexandre, DRANCÉ Martin, JELIN Rémy and NEUHAUS Abdelghani"
__copyright__ = "Copyright ?? December 2020" #TODO
__version__ = "1.0.0" 

# Libraries imports
import requests
import json
from xml.etree import ElementTree as ETree

# Local imports
from .ProteinPlotter import ProteinPlotter
from .PDBHandler import PDBHandler

class Protein():
    def __init__(self, id):
        self.m_id = id
        self.import_pdb_file_content()
        self.make_2D_prediction()
        self.gene = self.blast_figure = self.ramachandran_figure = None    
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
        self.prediction_figure = model.draw_2D_protein()
            
    def import_xml_data_from_uniprot(self):
        path = "{http://uniprot.org/uniprot}"
        response = requests.get("https://www.uniprot.org/uniprot/{}.xml".format(self.m_id))
        self.xml = ETree.fromstring(response.content)
        self.m_name = self.xml.find("{}entry/{}protein/{}recommendedName/{}fullName".format(path, path,path,path)).text
        self.gene = self.xml.find("{}entry/{}gene/{}name".format(path, path, path))
        if self.gene is None :
            self.gene = "N.A."
        else:
            self.gene = self.gene.text           
        self.m_species = self.xml.find("{}entry/{}organism/{}name".format(path, path,path)).text
        self.m_seq = self.xml.find("{}entry/{}sequence".format(path, path)).text
        self.m_length = self.xml.find("{}entry/{}sequence".format(path, path)).attrib['length']

            
    
    
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
   
    def get_blast_figure(self):
        return self.blast_figure
    
    def get_ramachandran_figure(self):
        return self.ramachandran_figure
    
