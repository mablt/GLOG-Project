import requests
import json

from .ProteinPlotter import *
from .PDBHandler import *

class Protein():
    def __init__(self, numero):
        self.m_id = numero
        # self.m_number = numero
        # print(self.m_number)
        
        # Get JSON file from request
        response = requests.get("https://swissmodel.expasy.org/repository/uniprot/%s.json"%self.m_id)
        if 'json' in response.headers.get('Content-Type'):
            self.m_json = response.json()
            
            # Add data from the JSON to the Protein Object
            
            # self.m_id = self.m_json['result']['uniprot_entries'][0]['ac']
            self.m_name = self.m_json['result']['uniprot_entries'][0]['id']
            self.m_length = self.m_json['result']['sequence_length']
            self.m_seq = self.m_json['result']['sequence']
        
        with open("./app/pdb/"+self.m_id+".pdb", 'r') as pdb_file_object:
            self.m_pdb = pdb_file_object.read()
            
        self.get_fasta_from_uniprot()
           
            
        # Request vers swissModel (plus utilisé car utilisation des ifhicers en local)
        # self.m_pdb =  requests.get("https://swissmodel.expasy.org/repository/uniprot/%s.pdb"%numero).text
        
    def get_fasta_from_uniprot(self):
        #code = "O48311"
        url = 'https://swissmodel.expasy.org/repository/uniprot/%s.fasta'%self.m_id
        # url = 'https://swissmodel.expasy.org/repository/uniprot/%s.fasta'%self.m_number
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
    
 
    def make_protein_plotter(self):
        load = PDBHandler(self.m_id, "./app/pdb/")
        data, length = load.data_creation()
        model = ProteinPlotter(data, length)
        fig = model.draw_2D_protein()
        return fig
    
    
    def get_pdb_file(self):
        return self.m_pdb

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

   
    # def get_json_from_uniprot(self):
    #     response = requests.get("https://swissmodel.expasy.org/repository/uniprot/%s.json"%self.m_number)
        
    #     if 'json' in response.headers.get('Content-Type'):
    #         self.m_json = response.json()
    #         print(self.m_json['result']['uniprot_entries'][0]['id'])
            
    #         self.m_id = self.m_json['result']['uniprot_entries'][0]['ac']
    #         self.m_name = self.m_json['result']['uniprot_entries'][0]['id']
    #         self.m_length = self.m_json['result']['sequence_length']
    #         self.m_seq = self.m_json['result']['sequence']

    # def set_attributes(self):
        # pass
        # print("DAdA")
        # print(self.m_json)
        # self.m_id = self.m_json['result']['uniprot_entries'][0]['ac']
        # self.m_name = self.m_json['result']['uniprot_entries'][0]['id']
        # self.m_length = self.m_json['result']['sequence_length']
        # self.m_seq = self.m_json['result']['sequence']
    
        
        
        
    # def execute(self):
    #     self.get_json_from_uniprot()
    #     self.set_attributes()
    #     # self.make_protein_plotter()
    

if __name__ == '__main__':
    test = Protein('P12345')
    # test.execute()