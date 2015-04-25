.. _dataio:

Importieren und Exportieren
===========================

In das Programm lassen sich bereits Datensätze importieren. Dazu verwendet man Textdateien, die aus einem Tabellenkalkulationsprogramm exportiert wurden. Dabei ist das CSV-Format am einfachsten zu handhaben.

Datenimport
-----------

Textdateien lassen sich mit dem Datenimport-Dialog öffnen. Dazu muss erst ein passender Datensatz erstellt werden (z.B. einen Flächendatensatz). Dieser wird dann ausgewählt und dann klickt man auf das Symbol für den Datenimport. Danach muss man eine Textdatei auswählen, die im nächsten Schritt geparst wird. 

.. figure:: ../_static/interface_file_parser_button.png
    :width: 300px
    :align: center
    :alt: screenshot with location of file parser button highlighted

    Der markierte Knopf öffnet den Datenimport-Dialog. Dazu muss auch ein bestehender Datensatz markiert sein.

Nachdem die Textdatei geöffnet wurde, öffnet sich der Datenparser-Dialog. Die Spalten in der Textdatei können den Spalten zugewiesen werden, die InnStereo veröffentlicht. Außerdem können Zeilen am Beginn der Datei übersprungen werden, die Meta-Daten enthalten.

.. figure:: ../_static/interface_file_parser_dialog.png
    :width: 400px
    :align: center
    :alt: screenshot of the file parser dialog

    Die Abbildung zeigt den Datenparser-Dialog.

Datenimport von anderen Programmen
----------------------------------

Die meisten älteren und noch verfügbaren Stereonetzprogramme verwenden keine speziellen Dateiformate, sondern setzen auf CSV-ähnliche Dateiformate. Diese können wie im vorherigen Abschnitt beschrieben, importiert werden. Die Dateiformate einiger Stereonetzprogramme werden im folgenden Abschnitt beschrieben.

TectonicsFP
^^^^^^^^^^^

TectonicsFP (Ortner et al., 2002) und seine anderen Versionen TektonikQB, TektonikFB and TectonicVB, benutzen CSV-Dateien mit verschiedenen Dateinamenerweiterungen. Die Dateien und deren Spaltenaufteilung sind in folgender Tabelle aufgelistet.

==============  ====================================================  ===============  =============================================================================
Dateiendung     Beschreibung                                          InnStereo        Spalten
==============  ====================================================  ===============  =============================================================================
pln             Fläche                                                Plane            Einfallr., Einf., Kommentar
lin             Linear                                                Linear           Einfallr., Einf., Kommentar
fpl             Störungsfläche                                        Faultplane       **(1)**, Einfallr. Fläche, Einf. Fläche, Einfallr. Linear, Einf. Linear, Kommentar
cor             Korrigierte Störungsf. (Lineare auf Fl. projeziert)   Faultplane       **(1)**, Einfallr. Fläche, Einf. Fläche, Einfallr. Linear, Einf. Linear, Kommentar
azi             Azimuth-Datensatz                                     Linear           Einfallrichtung
t**             PT-Axen-Datensatz                                     In Entwicklung   
==============  ====================================================  ===============  =============================================================================

    Die Tabelle zeigt die von TectonicsFP verwendeten Dateien. **(1)** Die erste Spalte der Störungsflächendatensätze ist eine zweistellige Zahl. Die erste Stelle speichert den Schersinn der Fläche ("0" or "5" = Unbekannt, "1" or "+" = Überschiebung, "2" or "-" = Abschiebung, "3" = Dextral, "4" = Sinistral). Die zweite Zahl steht für die Qualität oder Sicherheit des Messwertes. Die erste Stelle kann im Dateiparser-Dialog eingelesen werden, wenn man die Option "Tectonics FPL Notation" ankreuzt. Die zweite Stelle kann momentan nicht importiert werden.

Datenexport
-----------

Die Daten einzelner Datensätze lassen sich im CSV-Format exportieren. Dazu klickt man auf den Knopf in der linken unteren Leiste. Danach öffnet sich ein Dialog, in dem man den Speicherort und den Dateinamen festlegen kann. Der Knopf funktioniert nur, wenn genau ein Datensatz selektiert ist.

CSV-Dateien lassen sich mit zahlreichen anderen Programmen einfach importieren. Andere Dateiformate oder Datenbankanbindungen sind geplant.

.. figure:: ../_static/interface_file_export_button.png
    :width: 400px
    :align: center
    :alt: screenshot of the position of the file export button

    The hervorgehobene Knopf exportiert die Daten der momentan angewählten Ebene.

Literatur
---------

 - Beschreibung des `CSV-Formats <https://de.wikipedia.org/wiki/CSV_%28Dateiformat%29>`_ auf Wikipedia
 - Ortner, H., Reiter, F. & Acs, P. (2002). *Easy handling of tectonic data: the programs TectonicVB for Mac and TectonicsFP for Windows.* Computers & Geosciences(28/10), 1193-1200 (`doi:10.1016/S0098-3004(02)00038-9 <http://dx.doi.org/10.1016/S0098-3004%2802%2900038-9>`_).
 - Reiter, F. & Acs, P., (1996-2011). *TectonicsFP 1.75 - Computer Software for Structural Geology: Operating Manual.* Teil der TectonicsFP-Installation.
