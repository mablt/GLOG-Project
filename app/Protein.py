import requests
import json


class Protein():
    def __init__(self, numero):
        self.m_number = numero
        self.m_pdb = "https://swissmodel.expasy.org/repository/uniprot/%s.pdb"%numero
        self.m_json = self.m_id = self.m_name = self.m_length = self.m_seq = None 
    
    def get_json_from_uniprot(self):
        response = requests.get("https://swissmodel.expasy.org/repository/uniprot/%s.json"%self.m_number)
        # print(response.json.get("content-type"))
        # print(response.json())
        # response.json
        print(response.text)
        text = '{"success": "true", "status": 200, "message": "Hello"}'

        # exit()
        self.m_json = json.loads(text)

    def set_attributes(self):
        self.m_id = self.m_json['result']['uniprot_entries'][0]['ac']
        self.m_name = self.m_json['result']['uniprot_entries'][0]['id']
        self.m_length = self.m_json['result']['sequence_length']
        self.m_seq = self.m_json['result']['sequence']
    
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


# if __name__ == '__main__':
    # test = Protein('P12345')
    # test.execute()