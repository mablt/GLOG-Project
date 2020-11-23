import requests
import json

from .ProteinPlotterV1 import *
from .PDBHandlerV1 import *

class Protein():
    def __init__(self, numero):
        self.m_number = numero
        # self.m_pdb = open("path/"+self.m_number+".pdb", 'r')
        
        self.m_pdb =  requests.get("https://swissmodel.expasy.org/repository/uniprot/%s.pdb"%numero).text
        self.m_json = self.m_id = self.m_name = self.m_length = self.m_seq = None 
    
    def get_json_from_uniprot(self):
        response = requests.get("https://swissmodel.expasy.org/repository/uniprot/%s.json"%self.m_number)
        
        if 'json' in response.headers.get('Content-Type'):
            self.m_json = response.json()
            print(self.m_json['result']['uniprot_entries'][0]['id'])
            
            self.m_id = self.m_json['result']['uniprot_entries'][0]['ac']
            self.m_name = self.m_json['result']['uniprot_entries'][0]['id']
            self.m_length = self.m_json['result']['sequence_length']
            self.m_seq = self.m_json['result']['sequence']

    def set_attributes(self):
        pass
        # print("DAdA")
        # print(self.m_json)
        # self.m_id = self.m_json['result']['uniprot_entries'][0]['ac']
        # self.m_name = self.m_json['result']['uniprot_entries'][0]['id']
        # self.m_length = self.m_json['result']['sequence_length']
        # self.m_seq = self.m_json['result']['sequence']
    
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

    def execute(self):
        self.get_json_from_uniprot()
        self.set_attributes()
        # self.make_protein_plotter()


    def make_protein_plotter(self):
        load = PDBHandler(self.m_id, "./app/pdb/")
        data, length = load.data_creation()
        model = ProteinPlotter(data, length)
        fig = model.draw_2D_protein()
        return fig
        

# if __name__ == '__main__':
    # test = Protein('P12345')
    # test.execute()