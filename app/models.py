import requests
import json

########################### LIKE SERVER2 BEFORE ###########################

def getResponse(name):
    response = requests.get("https://swissmodel.expasy.org/repository/uniprot/%s.pdb" %name)
    # Add ?provider=swissmodel after json to get the SwissModel data
    # https://swissmodel.expasy.org/repository/uniprot/P07900.pdb?sort=seqsim to get the best 
    # homology model or experimental structure in PDB format sorted by sequence similarity
    return response.text


"""

NOT USED


# @app.route('/result', methods = ['POST', 'GET'])
def jsonPrint(obj):
    text = json.dumps(obj, sort_keys=True, indent=2)
    return text

# @app.route('/result', methods = ['POST', 'GET'])
def print_pdb(protein):

   # Get the JSON
   pdbBrutData = getResponse(protein)
   return pdbBrutData

   # # Get some useful informations from the BRUT json file
   # print("sequence :", jsonBrutData['result']['sequence'])               # Get the sequence
   # print('sequence length :', jsonBrutData['result']['sequence_length'])        # Get the sequence length
   # print("pdb file link :", jsonBrutData['result']['structures'][0]['coordinates'])       # Get the url of the pdb file
   # print("modelling model :", jsonBrutData['result']['structures'][0]['method'])       # Get the modelling method
   # print("protein number :", jsonBrutData['result']['uniprot_entries'][0]['ac'])       # Get the qualifier id
   # print("protein id :", jsonBrutData['result']['uniprot_entries'][0]['id'])       # Get the id of the protein
   # return pdbBrutData

"""

########################### LIKE SERVER1 BEFORE ###########################


"""
def getResponse(name):
    response = requests.get("https://swissmodel.expasy.org/repository/uniprot/%s.json" %name)
    # Add ?provider=swissmodel after json to get the SwissModel data
    # https://swissmodel.expasy.org/repository/uniprot/P07900.pdb?sort=seqsim to get the best 
    # homology model or experimental structure in PDB format sorted by sequence similarity
    return response

def jsonPrint(obj):
    text = json.dumps(obj, sort_keys=True, indent=2)
    return text

def print_pdb(protein):

   # Get the JSON
   pdbBrutData = getResponse(protein).json()

   # # Get some useful informations from the BRUT json file
   # print("sequence :", jsonBrutData['result']['sequence'])               # Get the sequence
   # print('sequence length :', jsonBrutData['result']['sequence_length'])        # Get the sequence length
   # print("pdb file link :", jsonBrutData['result']['structures'][0]['coordinates'])       # Get the url of the pdb file
   # print("modelling model :", jsonBrutData['result']['structures'][0]['method'])       # Get the modelling method
   # print("protein number :", jsonBrutData['result']['uniprot_entries'][0]['ac'])       # Get the qualifier id
   # print("protein id :", jsonBrutData['result']['uniprot_entries'][0]['id'])       # Get the id of the protein
   return pdbBrutData

"""