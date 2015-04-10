.. innsbruck_stereographic documentation master file, created by
   sphinx-quickstart on Sun Feb  8 22:32:13 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


.. image:: ../_static/logo_about.png


Welcome to the documentation of Innsbruck Stereographic!
========================================================

Innsbruck Stereographic (or InnStereo for a shorter name) is an open-source stereographic projection program, intended for usage in geology and structural geology. The program aims to be similar to TectonicsFP in usability and functionality.

The program is written in Python 3 and relies on `MPLStereonet <https://github.com/joferkington/mplstereonet>`_ for stereographic calculations. The plots are rendered using `Matplotlib <http://matplotlib.org/>`_ and many calculations rely on `Numpy <http://www.numpy.org/>`_. The graphical user interface is built using `GTK+ <http://www.gtk.org/>`_ and the `Glade <https://glade.gnome.org/>`_ rapid application development program.

The program is currently in early development and the source-code is tracked in `this Github repository <https://github.com/tobias47n9e/innsbruck-stereographic>`_. Due to the early stage of the development the documentation will still undergo frequent changes.

Contents:
---------
.. toctree::
   :numbered:
   :maxdepth: 2
   
   interface
   stereonet
   datasets
   formatting
   views
   dataio
   screenshots
   changelog


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

