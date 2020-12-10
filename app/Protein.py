#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Protein.py: Protein class of the GLOG Project.
"""

__author__ = "ALVES Marine, BOLTEAU Mathieu, CARRIAT Mélanie, CORNIER Alexandre, DRANCÉ Martin, JELIN Rémy and NEUHAUS Abdelghani"
__copyright__ = "Copyright (C) 2020, ALVES M., BOLTEAU M., CARRIAT M., CORNIER A., DRANCÉ M., JELIN R. and NEUHAUS A."
__license__ = "GNU GPL3"
__version__ = "1.0.0"

# Libraries imports
import requests
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
    """
    Class to represent a protein.

    ...

    Attributes
    ----------
    id                (str)       : Id of the protein
    name              (str)       : Name of the protein
    gene                (str)       : Name of the gene which the porotein come
    organism           (str)       : Name of the specie for the protein
    m_seq               (str)       : Sequence of the protein
    length            (int)       : Length of the protein
    xml                 (Element)   : XML Element of the XML file parsed
    pdb_content         (str)       : Content of the PDB file as a string
    blast_ids           (list)      : List of the ids of the three best hits of the Blast
    prediction_figure   (str)       : String which represent the base64 signature of the 2D prediction figure
    ramachandran_figure (str)       : String which represent the base64 signature of the ramachandran figure


    Methods
    -------
    import_pdb_file_content():
        Import the data (as string) from the PDB file of the protein and put it to 'pdb_content' variable
    make_2D_prediction():
        Make the 2D prediction and put the matplotlib figure object in 'prediction_figure' variable
    import_xml_data_from_uniprot():
        Import the data (as string) from the XML file of the protein parsed from a request
    make_ramachandran():
        Make the ramachandran for the protein
    make_blast():
        Make Blast for the protein and add the ids of the three first hits to 'self.blast_ids' variable
    transform_2D_prediction_figure(prediction_figure):
        Transform the 2D prediction figure into string of bytes
    transform_ramachandran_figure(ramachandran_figure)
        Transform the ramachandran figure to string of bytes
    get_attributes():
        Get all protein attributes without 'self.blast_ids' and 'self.ramachandran_figure'
    """

    def __init__(self, id):
        self.id = id
        self.import_pdb_file_content()
        self.make_2D_prediction()
        self.blast_ids = self.ramachandran_figure = None
        self.import_xml_data_from_uniprot()

    def import_pdb_file_content(self):
        """
        Import the data (as string) from the PDB file of the protein and put it to 'pdb_content' variable
        """
        with open("./app/pdb/"+self.id+".pdb", 'r') as pdb_file_object:
            self.pdb_content = pdb_file_object.read()

    def make_2D_prediction(self):
        """
        Make the 2D prediction and put the matplotlib figure object in 'prediction_figure' variable
        """
        load = PDBHandler(self.id, "./app/pdb/")
        data, length = load.data_creation()
        model = ProteinPlotter(data, length)
        figure = model.draw_2D_protein()
        encoded_prediction_figure = self.transform_2D_prediction_figure(figure)
        self.prediction_figure = encoded_prediction_figure

    def import_xml_data_from_uniprot(self):
        """
        Import the data (as string) from the XML file of the protein parsed from a request
        """
        path = "{http://uniprot.org/uniprot}"
        response = requests.get(
            "https://www.uniprot.org/uniprot/{}.xml".format(self.id))
        self.xml = ETree.fromstring(response.content)
        self.name = self.xml.find(
            "{}entry/{}protein/{}recommendedName/{}fullName".format(path, path, path, path)).text
        self.gene = self.xml.find(
            "{}entry/{}gene/{}name".format(path, path, path))
        if self.gene is None:
            self.gene = "N.A."
        else:
            self.gene = self.gene.text
        self.organism = self.xml.find(
            "{}entry/{}organism/{}name".format(path, path, path)).text
        self.m_seq = self.xml.find(
            "{}entry/{}sequence".format(path, path)).text
        self.length = self.xml.find(
            "{}entry/{}sequence".format(path, path)).attrib['length']

    def make_ramachandran(self):
        """
        Make the ramachandran for the protein
        """
        path = "./app/pdb/"+self.id+".pdb"
        data = phi_psi(path)  # ramachadran data
        # Create a tempfile to save the figure file
        figure = tempfile.TemporaryFile()
        plot(path, out=figure)
        # Put the byte-string of the figure in the 'self.ramachandran_figure' variable
        self.ramachandran_figure = self.transform_ramachandran_figure(figure)

    def make_blast(self):
        """
        Make Blast for the protein and add the ids of the three first hits to 'self.blast_ids' variable
        """
        query = Query(self.m_seq, query_type="sequence",
                      return_type="polymer_entity")
        search = query.search()
        self.blast_ids = list()
        for i in range(3):
            long_id = search["result_set"][i]["identifier"]
            id = long_id.split('_')[0]   # Remove '_1' at the end of the ID
            self.blast_ids.append(id)

    def transform_2D_prediction_figure(self, prediction_figure):
        """
        Transform the 2D prediction figure into string of bytes

        Args:
            prediction_figure (Figure): Matplotlib figure of the 2D prediction

        Returns:
            str: 2D prediction figure in bytes-string
        """
        # Transform the Figure object to bytes object
        img = io.BytesIO()
        prediction_figure.savefig(img, format='png', bbox_inches='tight')
        img.seek(0)
        # Encode to bytes object the figure bytes value
        encoded = base64.b64encode(img.getvalue())
        # Return the bytes figure as string
        return encoded.decode('utf-8')

    def transform_ramachandran_figure(self, ramachandran_figure):
        """
        Transform the ramachandran figure to string of bytes

        Args:
            ramachandran_figure (TemporaryFile): Temporary file which contains the ramachandran figure

        Returns:
            str: Ramachandran figure in bytes-string
        """
        ramachandran_figure.seek(0)
        encoded = base64.b64encode(ramachandran_figure.read())
        return encoded.decode('utf-8')

    def get_attributes(self):
        """
        Get all protein attributes without 'self.blast_ids' and 'self.ramachandran_figure'

        Returns:
            dict: Dictionnary which contains the attibutes of the protein
        """
        attributes = {
            "id": self.id,
            "name": self.name,
            "organism": self.organism,
            "length": self.length,
            "gene": self.gene,
            "pdb": self.pdb_content,
            "2D_prediction":self.prediction_figure,
        }
        return attributes

    def get_blast_ids(self):
        """
        Blast ids list getter

        Returns:
            list: List of the ids of the three better hits
        """
        return self.blast_ids

    def get_ramachandran_figure(self):
        """
        Ramachandran figure getter

        Returns:
            str: Ramachandran figure as bytes-string
        """
        return self.ramachandran_figure
