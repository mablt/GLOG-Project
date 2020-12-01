#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Protein.py: ProteinRepository class of the GLOG Project.

DESCRITPION #TODO
"""

__author__ = "ALVES Marine, BOLTEAU Mathieu, CARRIAT Mélanie, CORNIER Alexandre, DRANCÉ Martin, JELIN Rémy and NEUHAUS Abdelghani"
__copyright__ = "Copyright ?? December 2020" #TODO
__version__ = "1.0.0" 

# Local imports
from .Protein import Protein

class ProteinRepository():
    
    def __init__(self):
        self.proteins = dict()
        
    def add_protein(self, id):
        """Add a protein object to the repository

        Args:
            id (string): ID of the protein
        """
        if self.is_absent(id):
            protein = Protein(id)
            self.proteins[id] = protein
            
    def get_2D_prediction(self, id):
        """Get the 2D prediction figure of the protein with the ID 'id'

        Args:
            id (string): ID of the protein

        Returns:
            Object: Matplotlib figure of the 2D prediction structure of the protein
        """
        protein = self.proteins.get(id)
        # Creation de la figure dans l'objet Protein
        if protein.get_2D_prediction_figure() is None:
            protein.make_2D_prediction()
        return protein.get_2D_prediction_figure()
    
    
    def is_absent(self,id):
        """Check if the protein with the ID 'id' is absent of the repository

        Args:
            id (string): ID of the protein

        Returns:
            boolean: Boolean which represent the abscence or not of the protein in the repository
        """
        if id in self.proteins.keys():
            return False
        return True
        
        
    def get_protein_by_id(self, id):
        """Return the Protein object with the ID is 'id'

        Args:
            id (string): ID of the protein

        Returns:
            Protein: Protein object wanted
        """
        if self.is_absent(id):
            self.add_protein(id)
        return self.proteins.get(id)
    
    def get_protein_informations_by_id(self, id):
        protein = self.get_protein_by_id(id)
        data = {
            "name": protein.get_name(),
            "species": protein.get_species(),
            "length": protein.get_length(),
            "gene": protein.get_gene(),
            "pdb": protein.get_pdb(),
            "2D_prediction": protein.get_2D_prediction_figure(),
            "ramachandran": protein.get_ramachandran_figure()
        }
        return data
    
    def make_blast(self, id):
        # protein = self.proteins.get(id)
        # if protein.get_blast_figure() is None:
        #     protein.make_blast()
        # return protein.get_blast()
         
        # TODO
        
        pass
    
    def make_ramachandran(self, id):
        protein = self.proteins.get(id)
        if protein.get_ramachandran_figure() is None:
            protein.make_ramachandran()
        return protein.get_ramachandran_figure()