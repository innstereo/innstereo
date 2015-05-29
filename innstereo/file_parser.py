#!/usr/bin/python3

"""
This module contains the FileParseDialog-class.

The file-parse dialog is controlled by the FileParseDialog-class. The class
loads the GUI from the glade file and connects all the GUI signals.
"""

from gi.repository import Gtk
import re
import os


class FileParseDialog(object):

    """
    This class sets up the file-parse dialog and connects all its signals.

    The file parse dialog is loaded from the project Glade file. It contains
    a few buttons that control the parsing and the import of the data and
    a treeview that displays the result of the parsing. The method-names are
    defined in Glade and are connected to this class.
    """

    def __init__(self, text_file, layer_obj, redraw_plot,
                 append_plane, append_line, append_faultplane, main_window):
        """
        Initializes the file parser dialog and connects the signals.

        The GUI-layout is loaded from the project Glade file. The functions
        that the dialog needs to import the data and refresh the plot are
        assigned. Then the treestore and treeview are set up. A few buttons
        are hidden, depending on the layer that was chosen for the import. Then
        the signals are connected and the dialog does the first parsing of the
        file.
        """
        self.builder = Gtk.Builder()
        script_dir = os.path.dirname(__file__)
        rel_path = "gui_layout.glade"
        abs_path = os.path.join(script_dir, rel_path)
        self.builder.add_objects_from_file(abs_path,
            ("file_parse_dialog", "liststore_assign_columns",
             "adjustment_parse_start_line"))
        self.tfpl_dic = {"0": "ukn", "1": "up", "2": "dn", "3": "dex",
                         "4": "sin"}
        self.dialog = self.builder.get_object("file_parse_dialog")
        self.dialog.set_transient_for(main_window)
        self.redraw_plot = redraw_plot
        self.layer_obj = layer_obj
        self.append_plane = append_plane
        self.append_line = append_plane
        self.append_faultplane = append_faultplane
        self.file = text_file
        self.load_gui_elements()
        self.create_treeview()
        self.hide_buttons()
        self.builder.connect_signals(self)
        self.parse_file()

    def load_gui_elements(self):
        """
        Loads all the GUI elements that the dialog needs.

        The dialog needs to access the state of certain GUI elements
        to control the parsing and the import of the data. These elments
        are loaded with the builder.
        """
        self.combobox_plane_dipdir = self.builder.\
                                        get_object("combobox_plane_dipdir")
        self.combobox_plane_dip = self.builder.get_object("combobox_plane_dip")
        self.combobox_strat = self.builder.get_object("combobox_strat")
        self.combobox_line_dipdir = self.builder.\
                                        get_object("combobox_line_dipdir")
        self.combobox_line_dip = self.builder.get_object("combobox_line_dip")
        self.combobox_line_sense = self.builder.\
                                        get_object("combobox_line_sense")
        self.scr_win = self.builder.get_object("scrolledwindow_file_parser")
        self.grid_planes = self.builder.get_object("grid_planes")
        self.grid_linears = self.builder.get_object("grid_linears")

    def hide_buttons(self):
        """
        Hides certain buttons that are specific to a layer-type.

        Depending on the selected layer, this method will hide certain
        elements of the GUI. For plane-layers the grid containing line
        imports is hidden and vice versa.
        """
        self.grid_planes = self.builder.get_object("grid_planes")
        self.grid_linears = self.builder.get_object("grid_linears")
        layer_type = self.layer_obj.get_layer_type()
        if layer_type == "plane":
            self.grid_linears.hide()
        elif layer_type == "line":
            self.grid_planes.hide()

    def create_treeview(self):
        """
        Creates the viewport and adds it to the dialog window.

        The parsing dialog displays the parsing results in a TreeView.
        This requires setting up a TreeStore that has enough columns for a
        typical file to be imported. The TreeViewColumns are set up for text 
        and appended to the TreeView. The TreeView is then added to to
        the ScrolledWindow defined in Glade.
        """
        self.store = Gtk.ListStore(str, str, str, str, str, str, str, str)
        self.view = Gtk.TreeView(self.store)
        for x in range(8):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(str(x), renderer, text=x)
            column.set_alignment(0.5)
            column.set_expand(True)
            self.view.append_column(column)

        self.scr_win.add(self.view)
        self.dialog.show_all()

    def append_data(self, st_lst):
        """
        Receives a list of strings and appends them to the parsing TreeStore.

        This method receives a list of strings that are the result of the
        file parsing. The list corresponds to one row of the parsed file.
        If the row has less than 8 entries, a while-loop will append empty
        columns to it. Then the values are appended to the TreeStore.
        """
        while len(st_lst) < 8:
            st_lst.append("")
        self.store.append([st_lst[0], st_lst[1], st_lst[2], st_lst[3],
                          st_lst[4], st_lst[5], st_lst[6], st_lst[7]])

    def parse_file(self, start_line=0):
        """
        Parses the file according to the settings and updates the TreeView.

        The old parsing result are cleared from the TreeStore. Then each
        row of the file is re-iterated and all rows before the starting
        row are omitted. The rows are passed to the append_data-method.
        """
        self.store.clear()
        parse_file = open(self.file, "r")
        for key, line in enumerate(parse_file):
            if key < start_line:
                continue
            else:
                string_list = re.split(r"[;,]", line)
                self.append_data(string_list)

    def on_spinbutton_start_line_value_changed(self, spinbutton):
        """
        Gets the new start line and passes it to the parse_file method.

        If the user changes the starting line for the parsing, the new
        starting line will be passes to the parse_file method. This will
        result in all the lines, before the starting line, to be omitted.
        """
        start_line = spinbutton.get_value()
        self.parse_file(start_line)

    def run(self):
        """
        Shows the dialog.

        The dialog is a Gtk.Dialog and therefore has an intrinsic run()
        function. This results in the dialog appearing on the screen.
        """
        self.dialog.run()

    def on_file_parse_dialog_close(self, widget):
        # pylint: disable=unused-argument
        """
        Triggered when the dialog is closed. Hides the dialog.

        When the dialog is closed using the x-button, the dialog is hidden
        and no importing actions are triggered. The results of the parsing
        are lost.
        """
        self.dialog.hide()

    def on_file_parse_dialog_destroy(self, widget):
        # pylint: disable=unused-argument
        """
        Runs when the dialog is destroyed. Hides the dialog.

        When the dialog is destroyed it hidden and no other actions are taken.
        The results of the parsing are lost.
        """
        self.dialog.hide()

    def on_file_parse_dialog_response(self, widget, response):
        # pylint: disable=unused-argument
        """
        Executes when a response is triggered. Hides the dialog.

        When the dialog-response is triggered the dialog is hidden. No other
        actions are taken and the results of the parsing are lost.
        """
        self.dialog.hide()

    def on_button_parse_apply_clicked(self, button):
        # pylint: disable=unused-argument
        """
        Clicking apply appends the parsed data to the layer.

        When apply is clicked this method appends all the data to the
        liststore of the active layer. The method first gets all the column-
        numbers from the dialog. The column-numbers match the parsed-column
        with the internal column for the data (e.g. plane dip-direction is in
        the 3rd column in the parsed file, but needs to go into the 1st column
        of a plane-layer).
        """
        cb_pl_dipdir = self.combobox_plane_dipdir.get_active()
        cb_pl_dip = self.combobox_plane_dip.get_active()
        cb_pl_strat = self.combobox_strat.get_active()
        cb_ln_dipdir = self.combobox_line_dipdir.get_active()
        cb_ln_dip = self.combobox_line_dip.get_active()
        cb_ln_sense = self.combobox_line_sense.get_active()
        layer_store = self.layer_obj.get_data_treestore()
        layer_type = self.layer_obj.get_layer_type()
        self.checkbutton_tectonicsfpl = \
                            self.builder.get_object("checkbutton_tectonicsfpl")
        self.use_tfpl = self.checkbutton_tectonicsfpl.get_active()

        def iterate_over_planes(m, p, i):
            """
            Iterates over all parsed rows and adds them to a plane-layer.

            Replaces the values with a default so there is no IndexError.
            Calls the add_planar_feature function from the MainWindow class.
            """
            #m = model, p = path, i = itr
            if cb_pl_dipdir == -1:
                dipdir = 0
            else:
                dipdir = float(m[p][cb_pl_dipdir])
            if cb_pl_dip == -1:
                dip = 0
            else:
                dip = float(m[p][cb_pl_dip])
            if cb_pl_strat == -1:
                strat = ""
            else:
                strat = str(m[p][cb_pl_strat])
            self.append_plane(layer_store, dipdir, dip, strat)

        def iterate_over_lines(m, p, i):
            """
            Iterates over all parsed rows and adds them to a line-layer.

            Replaces the values with a default so there is no IndexError.
            Calls the add_linear_feature function from the MainWindow class.
            """
            #m = model, p = path, i = itr
            if cb_ln_dipdir == -1:
                dipdir = 0
            else:
                dipdir = float(m[p][cb_ln_dipdir])

            if cb_ln_dip == -1:
                dip = 0
            else:
                dip = float(m[p][cb_ln_dip])

            if cb_ln_sense == -1:
                sense = ""
            else:
                if self.use_tfpl is True:
                    sense = self.tfpl_dic[m[p][cb_ln_sense][0:1]]
                else:
                    sense = str(m[p][cb_ln_sense])

            self.append_line(layer_store, dipdir, dip, sense)

        def iterate_over_faultplanes(m, p, i):
            """
            Iterates over all parsed rows and adds them to a faultplane-layer.

            Replaces the values with a default so there is no IndexError.
            Calls the add_faultplane_feature function from the MainWindow class.
            """
            #m = model, p = path, i = itr
            if cb_pl_dipdir == -1:
                pl_dipdir = 0
            else:
                pl_dipdir = float(m[p][cb_pl_dipdir])

            if cb_pl_dip == -1:
                pl_dip = 0
            else:
                pl_dip = float(m[p][cb_pl_dip])

            if cb_ln_dipdir == -1:
                ln_dipdir = 0
            else:
                ln_dipdir = float(m[p][cb_ln_dipdir])

            if cb_ln_dip == -1:
                ln_dip = 0
            else:
                ln_dip = float(m[p][cb_ln_dip])

            if cb_ln_sense == -1:
                ln_sense = ""
            else:
                if self.use_tfpl is True:
                    ln_sense = self.tfpl_dic[m[p][cb_ln_sense][0:1]]
                else:
                    ln_sense = str(m[p][cb_ln_sense])

            self.append_faultplane(layer_store, pl_dipdir, pl_dip, ln_dipdir,
                                   ln_dip, ln_sense)

        if layer_type == "plane":
            self.store.foreach(iterate_over_planes)
        elif layer_type == "line":
            self.store.foreach(iterate_over_lines)
        elif layer_type == "faultplane":
            self.store.foreach(iterate_over_faultplanes)
        self.redraw_plot()
        self.dialog.hide()

    def on_button_cancel_clicked(self, button):
        # pylint: disable=unused-argument
        """
        Cancels the file parsing. Hides the dialog.

        Triggered when "Cancel" is clicked in the dialog. This method hides
        the dialog. No other actions are taken and the results of the parsing
        are lost.
        """
        self.dialog.hide()
