import numpy as np
from matplotlib.projections import PolarAxes, register_projection
from matplotlib.transforms import Affine2D, Bbox, IdentityTransform

#Source: http://stackoverflow.com/questions/2417794/how-to-make-the-angles-in-a-matplotlib-polar-plot-go-clockwise-with-0%C2%B0-at-the-to?lq=1

class NorthPolarAxes(PolarAxes):
    """
    A variant of PolarAxes where theta starts pointing north and goes
    clockwise.
    """
    name = "northpolar"

    class NorthPolarTransform(PolarAxes.PolarTransform):
        def transform(self, tr):
            xy   = np.zeros(tr.shape, np.float_)
            t    = tr[:, 0:1]
            r    = tr[:, 1:2]
            x    = xy[:, 0:1]
            y    = xy[:, 1:2]
            x[:] = r * np.sin(t)
            y[:] = r * np.cos(t)
            return xy

        transform_non_affine = transform

        def inverted(self):
            return NorthPolarAxes.InvertedNorthPolarTransform()

    class InvertedNorthPolarTransform(PolarAxes.InvertedPolarTransform):
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
