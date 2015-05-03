.. _changelog:

Änderungsprotokoll
==================

Momentan werden Versionsnummern nach dem folgenden Schema vergeben: Version 1.0 wird die erste stabile Version mit vollem Funktionsumfang sein. Alpha-Versionen geben frühe Einblicke in die Entwicklung. Beta-Versionen werden vergeben wenn das Programm weitgehend vollständig ist. Die jeweils aktuellste Version kann `auf dieser Seite <https://github.com/tobias47n9e/innstereo/releases>`_ heruntergeladen werden.

InnStereo v1.0-alpha.5
----------------------

 - [Feature] Dialog für Datenrotationen um eine beliebige Achse wurde hinzugefügt.
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
