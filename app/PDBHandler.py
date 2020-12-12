#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
PDBHandler.py: PDBHandler class of the GLOG Project.
"""

__author__ = "ALVES Marine, BOLTEAU Mathieu, CARRIAT Mélanie, CORNIER Alexandre, DRANCÉ Martin, JELIN Rémy and NEUHAUS Abdelghani"
__copyright__ = "Copyright (C) 2020, ALVES M., BOLTEAU M., CARRIAT M., CORNIER A., DRANCÉ M., JELIN R. and NEUHAUS A."
__license__ = " GNU General Public License v3"
__version__ = "1.0.0"

# Libraries imports
import os
from Bio.PDB import PDBParser
from Bio.PDB.DSSP import DSSP


class PDBHandler():
    """
    Class to extract and create informations from PDB file and XML request.

    ...

    Attributes
    ----------
    m_id                (str)       : Id of the protein
    m_folder            (str)       : Path to the PDB folder
    m_rawSeq            (list)      : temporary list that contains the raw sequence
    m_helixPos          (list)      : Contains sorted data for helixes
    m_sheetPos          (list)      : Contains sorted data for sheets
    m_tmpHelixPos       (list)      : Use to create m_helixPos
    m_tmpSheetPos       (list)      : Use to create m_sheetPos
    m_finalData         (list)      : Data that will be use by the ProteinPlotter class

    Methods
    -------
    load_data():
        Load all the pdb files in the folder. Create BIO.PDB.DSSP.DSSP object to stock each data's file
    get_secondary_structure():
        Retrieve the DSSP code letters of each amino acid of the protein
    transform_by_letter():
       Transform the data in entry (idStructure format) into a idConstruction style
    get_coordinates():
        Retrieves the position of each H and S in the m_rawSeq list
    split_list():
        Return the list index
    TopBottom():
        Return the first and last values of sublist of numbers
    get_coordinates_list_helix()
        Split the list base on the index in tmpHelixList
    get_coordinates_list_sheet():
        Split the list base on the index in tmpSheetList
    sorted_data2draw():
        Bubble sort
    data2draw():
          Merge helix and sheet coordinates into a list then do a bubble sort to sort sublists by coordinates
    data_creation():
        Create the final data, use with ProteinPlotter class
    """

    def __init__(self, id, folder):
        # Needed to initialize
        self.m_id = id  # id of the protein
        self.m_folder = folder  # folder which contains pdb files

        # Initialize during the creation of the instance
        # Data until we get a list looking like : [[1,2,3,4], [5,6,7]] returning [[1,4], [5,7]]
        self.m_rawSeq = None
        self.m_helixPos = None  # Contains sorted data for helixes
        self.m_sheetPos = None  # Contains sorted data for sheets
        self.m_tmpHelixPos = None   # Use to create m_helixPos
        self.m_tmpSheetPos = None   # Use to create m_sheetPos
        self.m_finalData = None     # Data that will be use by the ProteinPlotter class

    def load_data(self):
        """
        Load all the pdb files in the folder. Create BIO.PDB.DSSP.DSSP object to stock each data's file
        """
        stock = []
        pdb = self.m_folder + self.m_id + ".pdb"
        p = PDBParser()
        structure = p.get_structure("prot", pdb)
        model = structure[0]
        dssp = DSSP(model, pdb)
        stock.append(dssp)
        return stock

    def get_secondary_structure(self):
        """
        Retrieve the DSSP code letters of each amino acid of the protein
        """
        data = self.load_data()
        i = 0
        structure = []
        while(True):
            try:
                a_key = list(data[0].keys())[i]
                structure.append(data[0][a_key][2])
                i = i+1
            except IndexError:
                break
        self.m_rawSeq = structure

    def transform_by_letter(self):
        """
        Transform the data in entry (idStructure format) into a idConstruction style

        idStructure = {"H":"helix", "B":"sheet", "E":"sheet", "I":"coil", "S":"coil", "G":"coil", "T":"coil", "C":"coil"}
        idConstruction = {"H":"helix", "S":"sheet", "O":"other"} 
        """
        structure = []
        for i in range(len(self.m_rawSeq)):
            if self.m_rawSeq[i] == "H":
                structure.append("H")
            elif (self.m_rawSeq[i] == "B") or (self.m_rawSeq[i] == "E"):
                structure.append("S")
            else:
                structure.append("O")
        self.m_rawSeq = structure

    def get_coordinates(self):
        """
        Retrieves the position of each H and S in the m_rawSeq list
        Get 2 lists : one with each H position and a other one with S position
        """
        cooHelix = []
        cooSheet = []
        for i in range(len(self.m_rawSeq)):
            if self.m_rawSeq[i] == "H":
                cooHelix.append(i)
            elif self.m_rawSeq[i] == "S":
                cooSheet.append(i)
        self.m_tmpHelixPos = cooHelix
        self.m_tmpSheetPos = cooSheet

    def split_list(self, n):
        """
        Return the list index

        Args:
            n (list): list to get the indexes from

        Returns:
            (list): list of indexes
        """
        return [(x+1) for x, y in zip(n, n[1:]) if y-x != 1]

    def TopBottom(self, data):
        """
        Return the first and last values of sublist of numbers
        eg: [[1,2,3,4], [5,6,7]] return [[1,4], [5,7]]

        Args:
            data (list): list to get first and last values of sublist of numbers

        Returns:
            (list): list first and last values
        """
        res = []
        tmp = None
        for i in range(len(data)):
            if len(data[i]):
                tmp = data[i]
                res.append([tmp[0], tmp[-1]])
            else:
                res.append(data[i])
        return res

    def get_coordinates_list_helix(self):
        """
        Split the list base on the index in tmpHelixList

        Returns : 
            (list): a sorted list with sublists (eg: [[1], [3,7], [10, 12]])
        """
        my_index = self.split_list(self.m_tmpHelixPos)
        output = list()
        prev = 0
        for index in my_index:
            new_list = [x for x in self.m_tmpHelixPos[prev:] if x < index]
            output.append(new_list)
            prev += len(new_list)
        output.append([x for x in self.m_tmpHelixPos[prev:]])
        self.m_helixPos = output
        self.m_helixPos = self.TopBottom(self.m_helixPos)

    def get_coordinates_list_sheet(self):
        """
        Split the list base on the index in tmpSheetList

        Returns : 
            (list): a sorted list with sublists (eg: [[8,9], [15,17], [20, 22]])
        """
        my_index = self.split_list(self.m_tmpSheetPos)
        output = list()
        prev = 0
        for index in my_index:
            new_list = [x for x in self.m_tmpSheetPos[prev:] if x < index]
            output.append(new_list)
            prev += len(new_list)
        output.append([x for x in self.m_tmpSheetPos[prev:]])
        self.m_sheetPos = output
        self.m_sheetPos = self.TopBottom(self.m_sheetPos)

    def sorted_data2draw(self, a):
        """
        Bubble sort

        Args:
            a (list): list to sort

        Returns:
            (list): sorted list
        """
        n = len(a)
        # Traverser tous les éléments du tableau
        for i in range(n):
            for j in range(0, n-i-1):
                # échanger si l'élément trouvé est plus grand que le suivant
                if a[j][1][0] > a[j+1][1][0]:
                    a[j], a[j+1] = a[j+1], a[j]
        return a

    def data2draw(self):
        """
        Merge helix and sheet coordinates into a list named m_finalData. Then, do a bubble sort to sort sublists by coordinates
        eg : [['helix', [1]], ['helix', [10, 12]], ['sheet', [3]]]  INTO
             [['helix', [1]], ['sheet', [3]], ['helix', [10, 12]]] 
        """
        data = []
        for i in range(len(self.m_helixPos)):
            tmp = [None, None]
            tmp[0] = "helix"
            tmp[1] = self.m_helixPos[i]
            if tmp[1] != []:
                data.append(tmp)
        for i in range(len(self.m_sheetPos)):
            tmp = [None, None]
            tmp[0] = "sheet"
            tmp[1] = self.m_sheetPos[i]
            if tmp[1] != []:
                data.append(tmp)
        self.m_finalData = data
        self.m_finalData = self.sorted_data2draw(self.m_finalData)

    def data_creation(self):
        """
        Create the final data, use with ProteinPlotter class
        """
        self.get_secondary_structure()
        self.transform_by_letter()
        self.get_coordinates()
        self.get_coordinates_list_helix()
        self.get_coordinates_list_sheet()
        self.data2draw()
        return self.m_finalData, len(self.m_rawSeq)
