#!/usr/bin/python3

"""
This module contains the custom projection for a north-up polar plot.

The NorthPolarAxes-class is a polar projection that has its origin (0 degrees)
at the top and counts clockwise in the positive direction. This makes it
easier and fater to plot azimuth measurements. The class is called from the
PlotSettings class when the main window calls for a rose-diagram subplot. 
Source:
http://stackoverflow.com/questions/2417794/how-to-make-the-angles-in-a-
matplotlib-polar-plot-go-clockwise-with-0%C2%B0-at-the-to?lq=1
"""

import numpy as np
from matplotlib.projections import PolarAxes, register_projection
from matplotlib.transforms import Affine2D, Bbox, IdentityTransform


class NorthPolarAxes(PolarAxes):

    """
    Custom MPL-PolarAxes with theta 0 in the north and counting clockwise.

    This class inherits from, and overrides some of the methods of the
    Matplotlib PolarAxes-class. This class contains the NorthPolarTransfrom-
    and InvertedNorthPolarTransform-class. It also overrides the name-string
    and the '_set_lim_and_transforms'-function.
    """

    name = "northpolar"

    class NorthPolarTransform(PolarAxes.PolarTransform):

        """
        Custom normal transformation for the NorthPolarAxes.

        This class contains two function that override function in the
        Matplotlib PolarAxes.PolarTransform-class. The transformation is
        changed so 0 degrees is in the North and theta counts clockwise.
        """

        def transform(self, tr):
            xy = np.zeros(tr.shape, np.float_)
            t = tr[:, 0:1]
            r = tr[:, 1:2]
            x = xy[:, 0:1]
            y = xy[:, 1:2]
            x[:] = r * np.sin(t)
            y[:] = r * np.cos(t)
            return xy

        transform_non_affine = transform

        def inverted(self):
            return NorthPolarAxes.InvertedNorthPolarTransform()

    class InvertedNorthPolarTransform(PolarAxes.InvertedPolarTransform):

        """
        Custom inverted transformation for the NorthPolarAxes.

        This class contains two function that override function in the
        Matplotlib PolarAxes.InvertedPolarTransform-class. The transformation
        is changed so 0 degrees is in the North and theta counts clockwise.
        """

        def transform(self, xy):
            x = xy[:, 0:1]
            y = xy[:, 1:]
            r = np.sqrt(x*x + y*y)
            theta = np.arctan2(y, x)
            return np.concatenate((theta, r), 1)

        def inverted(self):
            return NorthPolarAxes.NorthPolarTransform()

    def _set_lim_and_transforms(self):
        PolarAxes._set_lim_and_transforms(self)
        self.transProjection = self.NorthPolarTransform()
        self.transData = (
            self.transScale + 
            self.transProjection + 
            (self.transProjectionAffine + self.transAxes))
        self._xaxis_transform = (
            self.transProjection +
            self.PolarAffine(IdentityTransform(), Bbox.unit()) +
            self.transAxes)
        self._xaxis_text1_transform = (
            self._theta_label1_position +
            self._xaxis_transform)
        self._yaxis_transform = (
            Affine2D().scale(np.pi * 2.0, 1.0) +
            self.transData)
        self._yaxis_text1_transform = (
            Affine2D().scale(1.0 / 360.0, 1.0) +
            self._yaxis_transform)

register_projection(NorthPolarAxes)
