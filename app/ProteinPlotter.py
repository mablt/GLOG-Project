import matplotlib.pyplot as plt
from .HelixPlotter import *
from .SheetPlotter import SheetPlotter
from .PDBHandler import PDBHandler
# from .Protein import Protein


class ProteinPlotter():

    def __init__(self, coo, leng):
        self.coordinates = coo
        self.seqLength = leng


    def draw_2D_protein(self):
        """
        Draw the protein 2D structure with data retrieve with the PDBHandler class
        """
        features = []
        for j in range (len(self.coordinates)):
            tmp = self.coordinates[j]
            min = 0
            max = 0
            if len(tmp) == 1:
                tmp[1] = min = max
                feature = seq.Feature("SecStr", [seq.Location(min, max)], {"sec_str_type" : tmp[0]})
                features.append(feature)
            else:
                min = tmp[1][0]
                max = tmp[1][-1]
                feature = seq.Feature("SecStr", [seq.Location(min, max)], {"sec_str_type" : tmp[0]})
                features.append(feature)

        annotation = seq.Annotation(features)
        fig = plt.figure(figsize=(9, 4))
        ax = fig.add_subplot(111)
        graphics.plot_feature_map(
            ax, annotation, multi_line=True, symbols_per_line=75, loc_range=(1,self.seqLength+1),
            # Register our drawing functions
            feature_plotters=[HelixPlotter(), SheetPlotter()]
        )
        fig.tight_layout()
        # plt.show()
        return fig



