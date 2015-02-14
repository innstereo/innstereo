.. _dataio:

Data Input and Output
=====================

In order to populate the layers or datasets with data, it is useful to do bulk import of data that has been prepared in a spreadsheet program. Innsbruck Stereographic can open various types of text files and text-based legacy formats from older stereographic projection programs.

Input
-----

The easiest way to add data to an existing layer is the file parse dialog. In order to use the file parser, one needs to create a dataset first (e.g. a plane dataset) and select it. The button opens a file chooser dialog, that one can use to locate the file on the hard-drive.

.. figure:: _static/interface_file_parser_button.png
    :width: 300px
    :align: center
    :alt: screenshot with location of file parser button highlighted

    The button for the file parser is in the folder icon in the highlighted area.

After a file has been choosen the parsing dialog opens. It includes an option to skip over lines at the beginning of the file, that usually contain metadata. The result of the parsing are shown in a table at the bottom of the dialog. Using the column numbers shows in that table, one can assign the columns to their respective counterparts of Innsbruck Stereographic.

.. figure:: _static/interface_file_parser_dialog.png
    :width: 400px
    :align: center
    :alt: screenshot of the file parser dialog

    The file parser dialog during a data-import. The columns in the data are assigned to the columns that Innsbruck Stereographic uses.

Input of legacy formats
-----------------------

The files of any program that outputs CSV-style files can be imported in Innsbruck Stereographic. The file formats of more prominent stereographic projection programs are listed below.

TectonicsFP
^^^^^^^^^^^

TectonicsFP (Ortner et al., 2002) and its predecessors TektonikQB, TektonikFB and TectonicVB, all use a variety of CSV files that can be easily imported using the file parser dialog. The assignment of the columns is the following:

==============  ====================================================  ===============  =============================================================================
File Extension  Despription                                           User Layer Type  Column Structure
==============  ====================================================  ===============  =============================================================================
pln             Planes                                                Plane            Dipdir, Dip, Comment
lin             Linears                                               Linear           Dipdir, Dip, Comment
fpl             Faultplanes                                           Faultplane       **(1)**, Plane Dipdir, Plane Dip, Linear Dipdir, Linear Dip, Comment
cor             Corrected Faultplanes (Linears flattened onto plane)  Faultplane       **(1)**, Plane Dipdir, Plane Dip, Linear Dipdir, Linear Dip, Comment
azi             Azimuth measurements                                  Linear           Dipdir
t**             PT-Axis calculation output                            In Development   
==============  ====================================================  ===============  =============================================================================

    This table shows how the file formats of TectonicsFP can be imported to Innsbruck Stereographic. **(1)** The first column of the "*.fpl" and "*.cor" files consists of a two-digit number. The first digit denotes the sense of movement of the fault ("0" or "5" = unknown, "1" or "+" = overthrust, "2" or "-" = downthrust, "3" = dextral strike-slip, "4" = sinistral strike-slip). The second digit denotes the quality or, or the confidence in the measurement. The first digit can be parsed using the "Tectonics FPL Notation" checkbox. The values will then be translated to the values that Innsbruck Stereographic uses. The second digit is currently not included in Innsbruck Stereographic.

Output
------

Data output is still under development.


Further Reading
---------------
 - Desription of `Comma-separated values <https://en.wikipedia.org/wiki/Comma-separated_values>`_ on Wikipedia
 - Ortner, H., Reiter, F. & Acs, P. (2002). *Easy handling of tectonic data: the programs TectonicVB for Mac and TectonicsFP for Windows.* Computers & Geosciences(28/10), 1193-1200 (`doi:10.1016/S0098-3004(02)00038-9 <http://dx.doi.org/10.1016/S0098-3004%2802%2900038-9>`_).
 - Reiter, F. & Acs, P., (1996-2011). *TectonicsFP 1.75 - Computer Software for Structural Geology: Operating Manual.* Bundled with the TectonicsFP installation.
