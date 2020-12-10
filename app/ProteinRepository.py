#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Protein.py: ProteinRepository class of the GLOG Project.
"""

__author__ = "ALVES Marine, BOLTEAU Mathieu, CARRIAT Mélanie, CORNIER Alexandre, DRANCÉ Martin, JELIN Rémy and NEUHAUS Abdelghani"
__copyright__ = "Copyright (C) 2020, ALVES M., BOLTEAU M., CARRIAT M., CORNIER A., DRANCÉ M., JELIN R. and NEUHAUS A."
__license__ = " GNU General Public License v3"
__version__ = "1.0.0"

# Local imports
from .Protein import Protein

class ProteinRepository():
    """
    Class to represent a protein repository.

    This class permits to communicate with the frontend. It execute all of the functionnalities 
    and return all needed informations for the frontend.
    ...

    Attributes
    ----------
    proteins            (dict)      : Dictionnary which contains proteins object. Keys are the id of the protein. Values are Protein objects.


    Methods
    -------
    add_protein(id):
        Add a protein object to the repository if is not already present
    get_2D_prediction(id)
        Get the 2D prediction figure of the protein with the ID 'id'
    is_absent(id):
        Check if the protein with the ID 'id' is absent of the repository
    get_protein_by_id(id)
        Return the Protein object with the ID 'id'
    get_protein_informations_by_id(id):
        Return protein informations of the protein with the ID 'id'
    get_blast(id):
        Get blast data of the protein with the ID 'id' and make it if it does not already done
    get_ramachandran(id):
        Get the ramachandran figure of the protein with the ID 'id' and it if it does not already done
    """
    
    def __init__(self):
        self.proteins = dict()
        
    def add_protein(self, id):
        """
        Add a protein object to the repository if is not already present

        Args:
            id (string): ID of the protein
        """
        if self.is_absent(id):
            protein = Protein(id)
            self.proteins[id] = protein
            
    def get_2D_prediction(self, id):
        """
        Get the 2D prediction figure of the protein with the ID 'id'

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
        """
        Check if the protein with the ID 'id' is absent of the repository

        Args:
            id (string): ID of the protein

        Returns:
            boolean: Boolean which represent the abscence or not of the protein in the repository
        """
        if id in self.proteins.keys():
            return False
        return True
        
        
    def get_protein_by_id(self, id):
        """
        Return the Protein object with the ID 'id'

        Args:
            id (string): ID of the protein

        Returns:
            Protein: Protein object wanted
        """
        if self.is_absent(id):
            self.add_protein(id)
        return self.proteins.get(id)
    
    def get_protein_informations_by_id(self, id):
        """
        Return protein informations of the protein with the ID 'id'

        Args:
            id (str): ID of the protein

        Returns:
            dict: Protein informations wanted
        """
        protein = self.get_protein_by_id(id)
        data = protein.get_attributes()
        return data
    
    def get_blast(self, id):
        """
        Get blast data of the protein with the ID 'id' and make it if it does not already done

        Args:
            id (str): ID of the protein

        Returns:
            list: List of the ids of the three better hits of the Blast
        """
        protein = self.proteins.get(id)
        if protein.get_blast_ids() is None:
            protein.make_blast()
        return protein.get_blast_ids()
        
    
    def get_ramachandran(self, id):
        """
        Get the ramachandran figure of the protein with the ID 'id' and it if it does not already done

        Args:
            id (str): ID of the protein

        Returns:
            str: Ramachandran figure as bytes-string
        """
        protein = self.proteins.get(id)
        if protein.get_ramachandran_figure() is None:
            protein.make_ramachandran()
        return protein.get_ramachandran_figure()