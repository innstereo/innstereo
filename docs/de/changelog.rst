.. _changelog:

Änderungsprotokoll
==================

Momentan werden Versionsnummern nach dem folgenden Schema vergeben: Version 1.0 wird die erste stabile Version mit vollem Funktionsumfang sein. Alpha-Versionen geben frühe Einblicke in die Entwicklung. Beta-Versionen werden vergeben wenn das Programm weitgehend vollständig ist. Die jeweils aktuellste Version kann `auf dieser Seite <http://innstereo.github.io/>`_ heruntergeladen werden.

InnStereo v1.0-beta.1
---------------------

 - [Feature] Projekte können jetzt als JSON-Dateien gespeichert und geladen werden.
 - [Feature] Das Programm hat jetzt einen Nachtmodus, in dem die Benutzeroberfläche in dunkelgrau dargestellt wird.
 - [Feature] Ein optionaler Hervorhebungsmodus erlaubt es Ebenen oder einzelne Objekte hervorzuheben.
 - [Feature] Ebenen können jetzt durch Ziehen und Ablegen mit der Maus verschoben werden. Das funktioniert auch zwischen mehreren Fenstern.
 - `[Bug] <https://github.com/tobias47n9e/innstereo/issues/20>`_ Zwei fehlende Mausschwebetexte hinzugefügt.
 - `[Bug] <https://github.com/tobias47n9e/innstereo/issues/24>`_ Ebenen-Gruppen werden jetzt über der ersten selektieren Eben hinzugefügt und automatisch ausgeklappt.

InnStereo v1.0-alpha.7
----------------------

 - `[Feature] <https://github.com/tobias47n9e/innstereo/issues/18>`_ Editiert man jetzt die letzte Spalte der letzten Zeile der Datenansicht, kann man mit drücken der Tabulator-Taste eine neue Zeile erstellen. Dies beschleunigt die Dateneingabe.
 - [Feature] Eine neue Funktion erlaubt es, die PT-Achsen von Störungs-Datensätzen zu berechnen.
 - [Feature] Die durschnittliche Richtung einer Gruppe von Linearen lässt sich jetzt berechnen.
 - [Bug] In der letzten Version wurden rotierte Datensätze in der Vorschau korrekt angezeigt, dem Projokt jedoch verdreht hinzugefügt. Dies sollte jetzt behoben sein.
 - [Bug] Ein neues Projekt lässt sich jetzt auch über das Dateimenü öffnen.
 - [Bug] Die Symbole für Pole und Lineare werden in der Legende jetzt nur noch einmal angezeigt.
 - [Bug] Kleinkreisdatensätze werden jetzt auch in der Legende angezeigt.
 - [Bug] Die Eigenvektor-Funktion liefert jetzt auch bei Linear-Datensätzen die richtigen Ergebnisse.

InnStereo v1.0-alpha.6
----------------------

 - [Bug] Rotationen über den Rand des Stereonetzes geben jetzt die richtigen Resultate. In der letzten Version wurden diese Punkte auf der oberen Hemisphäre dargestellt. 
 - [Bug] Flächen und Lineare rotieren jetzt in die gleiche Richtung.

InnStereo v1.0-alpha.5
----------------------

 - `[Feature] <https://github.com/tobias47n9e/innstereo/issues/13>`_ Dialog für Datenrotationen um eine beliebige Achse wurde hinzugefügt.
 - [Feature] Dialogfenster wurden überarbeitet (Struktur, Sensibilität, Schalter)
 - [Bug] Der Schalter der das zeichnen von Linearen an- un ausschaltet wird jetzt mit der richtigen Einstellung geladen.
 - `[Bug] <https://github.com/tobias47n9e/innstereo/issues/5>`_ Dialogfenster haben jetzt ein übergeordnetes Fenster.

InnStereo v1.0-alpha.4
----------------------

 - [Feature] Im Zentrum des Stereonetzes kann jetzt ein Kreuz angezeigt werden.
 - [Feature] Für die randliche Beschriftung des Stereonetzes kann jetzt zwischen einem Symbol für Norden, und Gradangaben gewechselt werden.
 - [Feature] Einzelne Datensätze lassen sich jetzt im CSV-Format exportieren.
 - [Feature] Die Statusleiste zeigt jetzt einige hilfreiche Meldungen und Warnungen.
 - [Feature] Der Ebenen-Dialog merkt sich jetzt die zuletzt angesehene Seite.
 - [Feature] Der Ebenen-Dialog kann jetzt auch über einen Knopf in der Menüleiste aufgerufen werden.
 - [Feature] Die Windows-Version hat jetzt ein zum Programm passendes Icon.
 - [Feature] Die Anzahl der Datensätze einer Ebene wird jetzt in der Legende angezeigt.
 - `[Bug] <https://github.com/tobias47n9e/innstereo/issues/7>`_ Die Ergebnisse von Berechnungen liegen jetzt immer im normalen Bereich für Stereonetze.
 - [Defaults] Die voreingestellte Standardabweichung für Konturierungen wurde auf 2 gesetzt (Vorher 3).
 - [Defaults] Das voreingestellte Aussehen von Linearen und Polpunkten wurde geändert.

InnStereo v1.0-alpha.3
----------------------

 - [Feature] Funktion, die den durchschnittlichen Schnittpunkt einer Gruppe von Flächen findet.
 - [Feature] Die Fläche, die normal zu einem Linear liegt, lässt sich jetzt berechnen.
 - [Bug] Einige verbleibende deutsche Strings wurden ins Englische übersetzt. Die Entwicklungsversionen werden auf Englisch sein um den Arbeitsaufwand geringer zu halten. Übersetzungen werden kurz vor der ersten 1.0-Version hinzugefügt.

InnStereo v1.0-alpha.2
----------------------

 - `[Bug] <https://github.com/tobias47n9e/innstereo/issues/1>`_ Ein Fehler in der Paketierung der Windows-Version wurde repariert, der die Verwendung des GtkFileChooserDialogs verhinderte. Dadurch konnten keine Abbildungen gespeichert werden und die Datenimportassistent nicht verwendet werden.
 - `[Bug] <https://github.com/tobias47n9e/innstereo/issues/2>`_ Eine Funktion, die den idealen Großkreis einer Gruppe von Linearen findet, ist jetzt verfügbar.

InnStereo v1.0-alpha.1
----------------------

 - [Feature] Planare Strukturen können als Großkreise und Polpunkte dargestellt werden.
 - [Feature] Lineare Strukturen können dargestellt werden.
 - [Feature] Kleinkreisverteilungen mit verschiedenen Öffnungswinkeln.
 - [Feature] Unterstüztung für flächentreue und winkeltreue Projektion.
 - [Feature] Mehrere Datensätze können verwaltet werden.
 - [Feature] Datensätze können auf verschiedene Arten konturiert werden.
 - [Feature] CSV-Dateien können importiert werden.
 - [Feature] Die Legende wird automatisch generiert.
 - [Feature] Für eine Gruppe von Linearen, lässt sich der ideale Großkreis berechnen.
 - [Feature] Datensätze können als Rosendiagramm dargestellt werden.
 - [Feature] Linien und Punkte haben zahlreiche Formatierungsoptionen.
