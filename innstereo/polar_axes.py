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
from matplotlib.axes import Axes
from matplotlib.patches import Wedge
import matplotlib.spines as mspines


class NorthPolarAxes(PolarAxes):
    # pylint: disable=no-init

    """
    Custom MPL-PolarAxes with theta 0 in the north and counting clockwise.

    This class inherits from, and overrides some of the methods of the
    Matplotlib PolarAxes-class. This class contains the NorthPolarTransfrom-
    and InvertedNorthPolarTransform-class. It also overrides the name-string
    and the '_set_lim_and_transforms'-function.
    """

    name = "northpolar"

    class NorthPolarTransform(PolarAxes.PolarTransform):
        # pylint: disable=no-init

        """
        Custom normal transformation for the NorthPolarAxes.

        This class contains two function that override function in the
        Matplotlib PolarAxes.PolarTransform-class. The transformation is
        changed so 0 degrees is in the North and theta counts clockwise.
        """

        def transform(self, tr):
            # pylint: disable=no-self-use,invalid-name
            """
            Overrides the transformation of the PolarTranform-class.

            This method overrides the same method in the PolarTransform-class.
            The new tranformation is North-up and counts clockwise positive.
            """
            xy = np.zeros(tr.shape, np.float_)
            t = tr[:, 0:1]  # pylint: disable=invalid-name
            r = tr[:, 1:2]  # pylint: disable=invalid-name
            x = xy[:, 0:1]  # pylint: disable=invalid-name
            y = xy[:, 1:2]  # pylint: disable=invalid-name
            x[:] = r * np.sin(t)
            y[:] = r * np.cos(t)
            return xy

        transform_non_affine = transform

        def inverted(self):
            # pylint: disable=no-self-use
            """
            Returns the inverted transformation class.

            The transformation also has to have a method to return the
            inverted transformation.
            """
            return NorthPolarAxes.InvertedNorthPolarTransform()

    class InvertedNorthPolarTransform(PolarAxes.InvertedPolarTransform):
        # pylint: disable=no-init

        """
        Custom inverted transformation for the NorthPolarAxes.

        This class contains two function that override function in the
        Matplotlib PolarAxes.InvertedPolarTransform-class. The transformation
        is changed so 0 degrees is in the North and theta counts clockwise.
        """

        def transform(self, xy):
            # pylint: disable=no-self-use,invalid-name
            """
            Overrides the transformation of the InvertedPolarTransform-class.

            This method overrides the same method in the
            InvertedPolarTransform-class. The new tranformation is North-up
            and counts clockwise positive.
            """
            x = xy[:, 0:1]  # pylint: disable=invalid-name
            y = xy[:, 1:]  # pylint: disable=invalid-name
            r = np.sqrt(x * x + y * y)  # pylint: disable=invalid-name
            theta = np.arctan2(y, x)
            return np.concatenate((theta, r), 1)

        def inverted(self):
            # pylint: disable=no-self-use
            """
            Returns the normal transformation class.

            The inverted transformation also has to have a method to return the
            normal transformation.
            """
            return NorthPolarAxes.NorthPolarTransform()

    def _set_lim_and_transforms(self):
        """
        Overrides the method with the same name in the PolarAxes-class.

        This method replaces the same method in the PolarAxes-class. It ensures
        that the limits and label placement fit the north-polar projection.
        """
        PolarAxes._set_lim_and_transforms(self)
        self.transProjection = self.NorthPolarTransform()
        # pylint: attribute-defined-outside-init,invalid-name
        self.transData = (
            self.transScale + 
            self.transProjection + 
            (self.transProjectionAffine + self.transAxes))
        # pylint: attribute-defined-outside-init,invalid-name
        self._xaxis_transform = (
            self.transProjection +
            self.PolarAffine(IdentityTransform(), Bbox.unit()) +
            self.transAxes)  # pylint: attribute-defined-outside-init
        self._xaxis_text1_transform = (
            self._theta_label1_position +
            self._xaxis_transform)  # pylint: attribute-defined-outside-init
        self._yaxis_transform = (
            Affine2D().scale(np.pi * 2.0, 1.0) +
            self.transData)  # pylint: attribute-defined-outside-init
        self._yaxis_text1_transform = (
            Affine2D().scale(1.0 / 360.0, 1.0) +
            self._yaxis_transform)  # pylint: attribute-defined-outside-init

register_projection(NorthPolarAxes)


class DipPolarAxes(PolarAxes):
    # pylint: disable=no-init

    """
    """

    name = "dippolar"

    def cla(self):
        PolarAxes.cla(self)
        self.set_thetagrids([0, 15, 30, 45, 60, 75, 90])

    def _gen_axes_patch(self):
        return Wedge((0.5, 0.5), 0.5, 270, 360)

    def _gen_axes_spines(self):
        path = Wedge((0, 0), 1.0, 270, 360).get_path()
        spine = mspines.Spine(self, 'circle', path)
        spine.set_patch_circle((0.5, 0.5), 0.5)
        return {'wedge':spine}

    class DipPolarTransform(PolarAxes.PolarTransform):
        # pylint: disable=no-init

        """
        """

        def transform(self, tr):
            # pylint: disable=no-self-use,invalid-name
            """
            """
            xy = np.zeros(tr.shape, np.float_)
            t = tr[:, 0:1]  # pylint: disable=invalid-name
            r = tr[:, 1:2]  # pylint: disable=invalid-name
            x = xy[:, 0:1]  # pylint: disable=invalid-name
            y = xy[:, 1:2]  # pylint: disable=invalid-name
            x[:] = r * np.sin(t + np.pi / 2)
            y[:] = r * np.cos(t + np.pi / 2)
            return xy

        transform_non_affine = transform

        def inverted(self):
            # pylint: disable=no-self-use
            """
            """
            return DipPolarAxes.InvertedDipPolarTransform()

    class InvertedDipPolarTransform(PolarAxes.InvertedPolarTransform):
        # pylint: disable=no-init

        """
        """

        def transform(self, xy):
            # pylint: disable=no-self-use,invalid-name
            """
            """
            x = xy[:, 0:1]  # pylint: disable=invalid-name
            y = xy[:, 1:]  # pylint: disable=invalid-name
            r = np.sqrt(x * x + y * y)  # pylint: disable=invalid-name
            theta = np.arctan2(y, x)
            return np.concatenate((theta, r), 1)

        def inverted(self):
            # pylint: disable=no-self-use
            """
            """
            return DipPolarAxes.DipPolarTransform()

    def _set_lim_and_transforms(self):
        """
        """
        PolarAxes._set_lim_and_transforms(self)
        self.transProjection = self.DipPolarTransform()
        # pylint: attribute-defined-outside-init,invalid-name
        self.transData = (
            self.transScale +
            self.transProjection +
            (self.transProjectionAffine + self.transAxes))
        # pylint: attribute-defined-outside-init,invalid-name
        self._xaxis_transform = (
            self.transProjection +
            self.PolarAffine(IdentityTransform(), Bbox.unit()) +
            self.transAxes)  # pylint: attribute-defined-outside-init
        self._xaxis_text1_transform = (
            self._theta_label1_position +
            self._xaxis_transform)  # pylint: attribute-defined-outside-init
        self._yaxis_transform = (
            Affine2D().scale(np.pi * 2.0, 1.0) +
            self.transData)  # pylint: attribute-defined-outside-init
        self._yaxis_text1_transform = (
            Affine2D().scale(1.0 / 360.0, 1.0) +
            self._yaxis_transform)  # pylint: attribute-defined-outside-init

register_projection(DipPolarAxes)
