#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SheetPlotter.py: SheetPlotter class of the GLOG Project.
"""

__author__ = "ALVES Marine, BOLTEAU Mathieu, CARRIAT Mélanie, CORNIER Alexandre, DRANCÉ Martin, JELIN Rémy and NEUHAUS Abdelghani"
__copyright__ = "Copyright (C) 2020, ALVES M., BOLTEAU M., CARRIAT M., CORNIER A., DRANCÉ M., JELIN R. and NEUHAUS A."
__license__ = " GNU General Public License v3"
__version__ = "1.0.0"

# Libraries imports
import biotite
import biotite.sequence as seq
import biotite.sequence.graphics as graphics


class SheetPlotter(graphics.FeaturePlotter):
    """
    Class to create protein's sheet visualization.

    ...

    Attributes
    ----------
    _head_width              (float)       : width of the head of the arrow that represents the sheet
    _tail_width             (float)       : width of the tail of the arrow that represents the sheet

    Methods
    -------
    matches():
        Check whether this class is applicable for drawing a feature
    draw():
        The drawing function that create helix visualization
    """

    def __init__(self, head_width=0.8, tail_width=0.5):
        self._head_width = head_width
        self._tail_width = tail_width


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
                if feature.qual["sec_str_type"] == "sheet":
                    return True
        return False

    def draw(self, axes, feature, bbox, loc, style_param):
        """
        The drawing function that create helix visualization

        Args:
            axes, feature, bbox, loc, style_param : matplotlib parameters to create the plot that will be gave by ProteinPlotter class

        Returns:
        """
        x = bbox.x0
        y = bbox.y0 + bbox.height/2
        dx = bbox.width
        dy = 0

        if  loc.defect & seq.Location.Defect.MISS_RIGHT:
            # If the feature extends into the prevoius or next line
            # do not draw an arrow head
            draw_head = False
        else:
            draw_head = True

        axes.add_patch(biotite.AdaptiveFancyArrow(
            x, y, dx, dy,
            self._tail_width*bbox.height, self._head_width*bbox.height,
            # Create head with 90 degrees tip
            # -> head width/length ratio = 1/2
            head_ratio=0.5, draw_head=draw_head,
            color=biotite.colors["orange"], linewidth=0
        ))