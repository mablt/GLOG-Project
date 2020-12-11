#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
HelixPlotter.py: HelixPlotter class of the GLOG Project.
"""

__author__ = "ALVES Marine, BOLTEAU Mathieu, CARRIAT Mélanie, CORNIER Alexandre, DRANCÉ Martin, JELIN Rémy and NEUHAUS Abdelghani"
__copyright__ = "Copyright (C) 2020, ALVES M., BOLTEAU M., CARRIAT M., CORNIER A., DRANCÉ M., JELIN R. and NEUHAUS A."
__license__ = " GNU General Public License v3"
__version__ = "1.0.0"

# Libraries imports
import biotite
import biotite.sequence as seq
import biotite.sequence.graphics as graphics
from matplotlib.patches import Rectangle
import numpy as np

class HelixPlotter(graphics.FeaturePlotter):
    """
    Class to create protein's helix visualization.

    ...

    Attributes
    ----------

    Methods
    -------
    matches():
        Check whether this class is applicable for drawing a feature
    draw():
        The drawing function that create helix visualization
    """

    def __init__(self):
        pass

    def matches(self, feature):
        """
        Check whether this class is applicable for drawing a feature

        Args:
            feature (class biotite.sequence.Feature) : Represent a single sequence feature that describes a functionnal part of a sequence

        Returns:
            Boolean whether the feature is an helix or not
        """
        if feature.key == "SecStr":
            if "sec_str_type" in feature.qual:
                if feature.qual["sec_str_type"] == "helix":
                    return True
        return False

    def draw(self, axes, feature, bbox, loc, style_param):
        """
        The drawing function that create helix visualization

        Args:
            axes, feature, bbox, loc, style_param : matplotlib parameters to create the plot that will be gave by ProteinPlotter class

        Returns:
        """
        # Approx. 1 turn per 3.6 residues to resemble natural helix
        n_turns = np.ceil((loc.last - loc.first + 1) / 3.6)
        x_val = np.linspace(0, n_turns * 2*np.pi, 100)
        # Curve ranges from 0.3 to 0.7
        y_val = (-0.4*np.sin(x_val) + 1) / 2

        # Transform values for correct location in feature map
        x_val *= bbox.width / (n_turns * 2*np.pi)
        x_val += bbox.x0
        y_val *= bbox.height
        y_val += bbox.y0

        # Draw white background to overlay the guiding line
        background = Rectangle(
            bbox.p0, bbox.width, bbox.height, color="white", linewidth=0
        )
        axes.add_patch(background)
        axes.plot(
            x_val, y_val, linewidth=2, color=biotite.colors["dimgreen"]
        )