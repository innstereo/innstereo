.. _changelog:

Changelog
=========

Versioning will work this way. Alpha releases will be done, so people can test early interface design decisions. Beta releases will done after the program is more mature. Eventually this will lead to the first 1.0 release. Download the most recent release from `this page <https://github.com/tobias47n9e/innstereo/releases>`_.

InnStereo v1.0-alpha.6
----------------------

 - [Bug] Rotations across stereonet boundaries leading to false results fixed. Points were falsely plotted on the upper hemisphere.
 - [Bug] Planes and linears now rotate in same direction.

InnStereo v1.0-alpha.5
----------------------

 - `[Feature] <https://github.com/tobias47n9e/innstereo/issues/13>`_ Data-Rotation-Dialog implemented.
 - [Feature] Improved dialog structure (switches, sensitivity, layout).
 - [Bug] Fixed loading the setting of line drawing switch which was always on.
 - `[Bug] <https://github.com/tobias47n9e/innstereo/issues/5>`_ Fixed dialog windows not having a transient parent set.

InnStereo v1.0-alpha.4
----------------------

 - [Feature] Stereonet can now show a center cross for easier readability of the data.
 - [Feature] Stereonet can now either show a North-symbol or the degrees around the edges.
 - [Feature] Data can be exported as CSV-files.
 - [Feature] Statusbar now displays some helpful messages and warnings.
 - [Feature] The layer-properties dialog now remembers the active page for each layer.
 - [Feature] Layer properties can now also be accessed by pressing on a toolbar-button.
 - [Feature] The builds for Windows now have a more identifiable icon.
 - [Feature] The number of datasets are now shown for each layer in the legend.
 - `[Bug] <https://github.com/tobias47n9e/innstereo/issues/7>`_ Fixed the issue, that caused calculations to yield values outside of the normal range of degrees.
 - [Defaults] Changed the default standard-deviations for contouring to 2 (previously 3).
 - [Defaults] Some changes to the default appearance of linears and poles.

InnStereo v1.0-alpha.3
----------------------

 - [Feature] Function to calculate the intersection of a group of planes.
 - [Feature] Calculate the plane that lies normal to a linear.
 - [Bug] Fixed some strings in the user interface that were not English. Localization of the program will be done as soon as time permits.

InnStereo v1.0-alpha.2
----------------------

 - `[Bug] <https://github.com/tobias47n9e/innstereo/issues/1>`_ Fixed issue that prevented any operations that required the GtkFileChooserDialog under Windows. This prevented saving a figure and choosing a file for file-parsing.
 - `[Bug] <https://github.com/tobias47n9e/innstereo/issues/2>`_ Fixed unresponsive find best-fitting plane button.

InnStereo v1.0-alpha.1
----------------------

 - [Feature] Plot planar structures as great circles or poles.
 - [Feature] Plot linear structures.
 - [Feature] Plot conical distributions as small circles.
 - [Feature] Switch between equal area and equal angle projection.
 - [Feature] Datasets have basic layer management.
 - [Feature] Datasets can be contoured.
 - [Feature] Import CSV-files into a layer.
 - [Feature] Legend is dynamically generated.
 - [Feature] Calculate the best-fitting plane for a set of linears.
 - [Feature] Rose diagram.
 - [Feature] Lines and markers have most formatting options that are possible in matplotlib.
