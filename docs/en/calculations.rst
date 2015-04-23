.. _calculations:

Calculations
============

InnStereo can perform a number of calculations for common tasks that occur when working with spatial data. In structural geology many geometries are connected to conjugated geomtries by a simple relationship (when ignoring natural variation). For example the stretching axis will always lie more or less 90° to the necking-axis of a boudin. That means that a statistical meaningful sample of necking-axis can be used to find the stretching direction, even if structures like stretching lineations are absent.

The following sections outline some of the currently available calculations. Calculations will always use all the selected layers as a data-source. If different layer-types are selected, the calculation will not be performed.

The results of a calculation are always added to the project as a new layer. The new layer is independent, and changes to the source-layer are not passed on to the result-layer.

.. _plane-intersection:

Intersection of Planes
----------------------

This calculations yields the average intersection of a set of planes. The intersection should lie in the area where most great-circles intersect.

.. _best-fitting-plane:

Best-Fitting Plane
------------------

The best-fitting plane can be calculated for a set of linears. This will yield a great circle that will pass through as many points as possible. The resulting plane will be added to the project as a plane layer.

.. _eigenvector:

Eigenvector and Eigenvalue
--------------------------

This method calculates the 3 eigenvectors and eigenvalues of a dataset. The algorithm will check if plane-layers or line-layers are selected. The results are added to the project as a new layer. The legend will be updated to show the 3 vectors in dip-direction/dip format with the 3 eigenvalues in parentheses.

.. _copy-poles:

Copy Poles
----------

This calculation will copy the poles of a plane-layer and adds them to the project as a new line layer.

.. _normal-planes:

Normal Planes
-------------

This method calculates the planes that lie normal to a set of linears and adds the resulting planes as a new layer to the project. This can be used to calculate the cross-section plane from a fold-axis.

.. _calculations-further-reading:

Further Reading
---------------


