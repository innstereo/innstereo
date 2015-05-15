.. _stereonet:

Stereonetz
==========

*Stereonetze* oder *Stereographische Projektionen* (auch *Lagenkugel* und *Lagenkugelprojektion*) sind eine der wichtigsten Darstellungsarten für raumbezogene Daten in der Strukturgeologie. Ihr Vorteil liegt darin, dass jede beliebige Orientierung im Raum in einer Ebene dargestellt werden kann. Am häufigsten wird dabei die flächentreue Projektion verwendet.

In der Geologie verwendet man zumeist die Einfallrichtung und das Einfallen um eine Struktur zu erfassen. Diese beiden Angabe in belieber Reihenfolge, reichen aus um eine Struktur in ihrer räumlichen Lage zu beschreiben. Die Einfallrichtung wird relativ zum geographischen Nordpol bestimmt, wobei die Winkel im Uhrzeigersinn ansteigen. Das Einfallen ist ein Tiefenwinkel, der relativ zur Horizontalebene nach unten gemessen wird. Beide Werte lassen sich mit einem Geologenkompass in einem Arbeitsschritt bestimmen.

Die Einfallrichtung wird immer mit drei Stellen angegeben, um sie vom zweistelligen Einfallen zu unterscheiden. Eine Lage einer Struktur die nach Osten mit 45° einfällt kann deswegen entweder mit 090/45 oder mit 45/090 eindeutig beschrieben werden. Für Strukturen die eine Richtung haben (z.B. Strömungsrichtung einer sedimentären Struktur) oder eine Magnitude haben (z.B. ein Versatz) müssen zusätzliche Angaben notiert werden.

Projektionen
------------

Flächentreue-Projektion
^^^^^^^^^^^^^^^^^^^^^^^

Für die meisten Fragestellungen in der Geologie ist es von Vorteil eine räumlich gleichmäßige Datenverteilung zu betrachten. Die dafür geeignetste Projektion ist die *flächentreue Azimutalprojektion* (oder *Lambert'sche Azimutalprojektion*). In der Geologie spricht man auch vom Schmidt'schen Netz (benannt nach Walter Schmidt).

.. figure:: ../_static/equal_area_small_circles.png
    :width: 400px
    :align: center
    :alt: equal area stereonet with small circles showing consistent size

    Diese Abbildung zeigt eine Reihe von Kleinkreisen mit einem Radius von 10°. Die Größe der Kreise bleibt über den gesamten Bereich relativ gut erhalten, während aufgrund der Winkelverzerrung die Kreise gegen den Rand hin zu Ellipsen verzerrt werden.

Transformation
~~~~~~~~~~~~~~

Aus einer Messung von Längen- und Breitengraden berechnen sich die X- und Y-Koordinaten der äquatorialen Lambert-Projektion aus folgenden Formeln (Snyder 1987):

.. math::

    x = Rk \cos(\phi) \sin(\lambda - \lambda_{0})

.. math::

    y = Rk \sin(\phi)

Mit k gleich:

.. math::

    k = \sqrt{\frac{2}{1 + \cos(\phi) \cos(\lambda - \lambda_{0})}}

Die Variablen stehen für:

 * R . . . Radius
 * ϕ . . . Breitengrad
 * λ . . . Längengrad
 * λ₀ . . . Zentralmeridian (y-Achse)

Die inverse Transformation, berechnet aus den XY-Koordinaten die Längen- und Breitengrade:

.. math::

    \phi = \arcsin \left[ \cos (c) \sin (\phi_{1}) + \left(\frac{y \sin(c) \cos(\phi_{1})} {\rho}\right) \right]

Für den Längengrad wird abhängig vom Breitengrad eine dieser drei Formeln verwedent:

Für Φ₁ gleich +90°:

.. math::

    \lambda = \lambda_{0} + \arctan \left[ \frac{x}{-y} \right]

Für Φ₁ gleich -90°:

.. math::

    \lambda = \lambda_{0} + \arctan \left[ \frac{x}{y} \right]

Für alle anderen Breitengrade verwendet man:

.. math::

    \lambda = \lambda_{0} + \arctan \left[ \frac{x \sin(c)}{\rho \cos(\phi_{1}) \cos(c) - y \sin(\phi_{1}) \sin(c)} \right]

Dabei gilt:

.. math::

    \rho = \sqrt{x^{2} + y^{2}}

.. math::

    c = 2 \arcsin \left[ \frac{\rho}{2 R} \right]


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

