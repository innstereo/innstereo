.. _stereonet:

Stereonetz
==========

*Stereonetze* oder *Stereographische Projektionen* sind eine der wichtigsten Darstellungsarten für raumbezogene Daten in der Strukturgeologie. Am häufigsten wird dabei die flächentreue Projektion verwendet.

Projektionen
------------

Flächentreue-Projektion
^^^^^^^^^^^^^^^^^^^^^^^

Für die meisten Fragestellungen in der Geologie ist es von Vorteil eine räumlich gleichmäßige Datenverteilung zu betrachten. Die dafür geeignetste Projektion ist die *stereographische Projektion*. In der Geologie spricht man auch vom Schmidt'schen Netz (benannt nach Walter Schmidt).

.. figure:: ../_static/equal_area_small_circles.png
    :width: 400px
    :align: center
    :alt: equal area stereonet with small circles showing consistent size

    Diese Abbildung zeigt eine Reihe von Kleinkreisen mit einem Radius von 10°. Die Größe der Kreise bleibt über den gesamten Bereich relativ gut erhalten, während aufgrund der Winkelverzerrung die Kreise gegen den Rand hin zu Ellipsen verzerrt werden.

Die X- und Y-Koordinaten berechnen sich aus den Längen- und Breitengraden aus dieser Formel:

.. math::

    x = Rk \cos(\phi) \sin(\lambda - \lambda_{0} \\
    y = Rk \sin(\phi) \\

Mit k gleich:

.. math::

    k = \frac{2 k_{0}}{1 + \cos(\phi) \cos(\lambda - \lambda_{0}}

Die Variablen stehen für:

.. math::

    R = Radius
    \phi = Breitengrad \\
    \lambda = Längengrad \\
    \lambda_{0} = Zentralmeridian (y-Achse) \\
    k_{0} = Skalierungsfaktor (normalerweise 1.0)

Die inverse Transformation, berechnet aus den XY-Koordinaten die Längen- und Breitengrade:

.. math::

    \phi = \arcsin{[}\cos (c) \sin (\phi_{1}) + (\frac{y \sin(c) \cos(\phi_{1})} {\rho}) {]}

Für den Längengrad wird abhängig vom Breitengrad eine dieser drei Formeln verwedent:

Für Φ₁ gleich +90°:

.. math::

    \lambda = \lambda_{0} + \arctan{[} \frac{x}{-y} {]}

Für Φ₁ gleich -90°:

.. math::

    \lambda = \lambda_{0} + \arctan{[} \frac{x}{y} {]}

Für alle anderen Breitengrade verwendet man:

.. math::

    \lambda = \lambda_{0} + \arctan{[} \frac{x \sin(c)}{\rho \cos(\phi_{1}) \cos(c) - y \sin(\phi_{1}) \sin(c)} {]}


Winkeltreue-Projektion
^^^^^^^^^^^^^^^^^^^^^^

.. figure:: ../_static/equal_angle_small_circles.png
    :width: 400px
    :align: center
    :alt: equal angle stereonet with small circles showing inconsistent size

    -

Literatur
---------

 - John P. Snyder (1987): `Map Projections - A Working Manual <http://pubs.er.usgs.gov/publication/pp1395>`_
 - `Flächentreue Azimutalprojektion <https://de.wikipedia.org/wiki/Fl%C3%A4chentreue_Azimutalprojektion>`_ auf Wikipedia
 - `Schmidt'sches Netz <https://de.wikipedia.org/wiki/Schmidtsches_Netz>`_ auf Wikipedia
 - `Wulff'sches Netz <http://de.wikipedia.org/wiki/Wulffsches_Netz>`_ auf Wikipedia
 - `Georgij Viktorovich Wulff <https://www.wikidata.org/wiki/Q907171>`_  auf Wikidata 
 - `Walter Schmidt <https://www.wikidata.org/wiki/Q15979728>`_ auf Wikidata

