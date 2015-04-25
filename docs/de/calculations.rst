.. _calculations:

Berechnungen
============

InnStereo kann eine Reihe von Berechnungen ausführen, die typisch für strukturgeologische Fragestellungen sind und für die Verarbeitung von raumbezogenen Daten eine Erleichterung sind. Konjugierte Strukturen sind im Raum oft durch einfache geometrische Beziehungen verknüpft. Ein Beispiel sind Neckingachsen von Boudins, die immer 90° zur Streckungsachse liegen. Ein statistische aussagkräftiger Datensatz in Kombination mit einer Berechnung kann so die Streckungsachse berechnen auch wenn direkte Messungen von Streckungslinearen nicht möglich sind.

Die Berechnung von raumbezogenen Daten ist oft aufwendig. InnStereo versucht solche Berechnungen möglichst mit nur einem Mausklick abrufbar zu machen. Die folgenden Abschnitte erklären die bereits verfügbaren Berechnungen. Weitere Berechnungen sind in der Entwicklung.

Berechnungen funktionieren nur, wenn nur Ebenen eines Typs (z.B. nur Flächen) selektiert sind. Die Ergebnisse einer Berechnung werden immer als neuer Datensatz dem Projekt hinzugefügt. Der neue Datensatz ist vom alten unabhängig und Änderungen am Ausgangsdatensatz werden nicht an den resultierenden Datensatz weitergegeben.

.. _plane-intersection:

Flächenintersektion
-------------------

Die Berechnung lieftert die Insektion einer Flächenschar. Im Stereonetz ist das der Punkt an dem sich die Großkreise schneiden. Die Berechnung kann verwendet werden um die Faltenachse aus der Messung der Schenkel abzuleiten. Ein anderes Beispiel ist die Berechnung des Intersektionslinears zweier Schieferungen.

.. _best-fitting-plane:

Gemeinsamer Großkreis
---------------------

Der gemeinsame Großkreis kann für eine Gruppe von Linearen berechnet werden. Das Ergebnis ist der Großkreis, auf dem die meisten Lineare liegen.

.. _eigenvector:

Eigenvektoren und Eigenwerte
----------------------------

Diese Methode berechnet die 3 Eigenvektoren und Eigenwerte eines Datensatzes. Der Datensatz unterscheidet automatisch ob Flächen oder Lineare selektiert sind. Das Ergebnis wird als Ebene dem Projekt hinzugefügt. Die Legende zeigt neben dem Symbol der Vektoren, die Einfallrichtung und das Einfallen der Vektoren und deren Eigenwerte in Klammern.

.. _copy-poles:

Flächenpole
-----------

Diese Berechnung kopiert die Flächenpole in eine eigenen Linear-Ebene.

.. _normal-planes:

Normalflächen
-------------

Diese Methode berechnet die Flächen, die normal zu den selektierten Lineare liegen.

.. _calculations-further-reading:

Literatur
---------


