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
        self.gene = None
        self.import_json_data_from_uniprot()
        self.import_fasta_data_from_uniprot()
        
        # self.import_xml_data_from_uniprot()
            
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
        
    def import_json_data_from_uniprot(self):
        response = requests.get("https://swissmodel.expasy.org/repository/uniprot/%s.json"%self.m_id)
        if 'json' in response.headers.get('Content-Type'):
            self.m_json = response.json()
            # Add data from the JSON to the Protein Object
            self.m_name = self.m_json['result']['uniprot_entries'][0]['id']
            self.m_length = self.m_json['result']['sequence_length']
            self.m_seq = self.m_json['result']['sequence']

        
    def import_fasta_data_from_uniprot(self):
        url = 'https://swissmodel.expasy.org/repository/uniprot/%s.fasta'%self.m_id
        r = requests.get(url)
        texte = r.text

        # Get the species name (between 0S)
        start = texte.find("OS") + len("OS")
        end = texte.find("\n")
        substring = texte[start:end]

        espece = []
        for i in range(len(substring)):
            espece.append(substring[i])
        self.m_species = [''.join(espece)]
        self.m_species[0] = self.m_species[0] + " ."

        if "GN" in self.m_species[0]:
            start = substring.find("=") + len("=")
            end = substring.find("GN")
            self.m_species = substring[start:end]
        else:
            start = substring.find("=") + len("=")
            end = substring.find(" .")
            self.m_species = substring[start:end]
            
        # Get the protein name (between a space and the OS=)
        start = texte.find(" ") + len(" ")
        end = texte.find("OS")
        self.m_protein = texte[start:end]     
    
    def import_xml_data_from_uniprot(self):
        path = "{http://uniprot.org/uniprot}"
        response = requests.get("https://www.uniprot.org/uniprot/{}.xml".format(self.m_id))
        self.xml = ETree.fromstring(response.content)
        self.m_name = self.xml.find("{}entry/{}protein/{}recommendedName/{}fullName".format(path, path,path,path)).text
        self.gene = self.xml.find("{}entry/{}gene/{}name".format(path, path,path)).text
        self.m_species = self.xml.find("{}entry/{}organism/{}name".format(path, path,path)).text
        self.m_seq = self.xml.find("{}entry/{}sequence".format(path, path)).text
        self.m_length = self.xml.find("{}entry/{}sequence".format(path, path)).attrib['length']

            
    
    
    def get_pdb_file(self):
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
   

    
