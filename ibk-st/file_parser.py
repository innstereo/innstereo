#!/usr/bin/python3

from gi.repository import Gtk
import re

class FileParseDialog(object):
    """
    This class handles the input and output of the file-parser dialog.
    """
    def __init__(self, text_file, layer_obj, redraw_plot,
                 append_plane, append_line, append_faultplane):
        """
        Initializes the file parser dialog and connects the signals.
        """
        self.builder = Gtk.Builder()
        self.builder.add_objects_from_file("gui_layout.glade",
            ("file_parse_dialog", "liststore_assign_columns",
             "adjustment_parse_start_line"))
        self.dialog = self.builder.get_object("file_parse_dialog")
        self.combobox_plane_dipdir = \
                        self.builder.get_object("combobox_plane_dipdir")
        self.combobox_plane_dip = self.builder.get_object("combobox_plane_dip")
        self.combobox_strat = self.builder.get_object("combobox_strat")
        self.combobox_line_dipdir = self.builder.get_object("combobox_line_dipdir")
        self.combobox_line_dip = self.builder.get_object("combobox_line_dip")
        self.combobox_line_sense = self.builder.get_object("combobox_line_sense")
        self.sw = self.builder.get_object("scrolledwindow_file_parser")
        self.grid_planes = self.builder.get_object("grid_planes")
        self.grid_linears = self.builder.get_object("grid_linears")
        self.redraw_plot = redraw_plot
        self.layer_obj = layer_obj
        self.append_plane = append_plane
        self.append_line = append_plane
        self.append_faultplane = append_faultplane
        self.file = text_file
        self.create_treeview()
        self.hide_buttons()
        self.builder.connect_signals(self)
        self.parse_file()

    def hide_buttons(self):
        """
        Hides the buttons of the interface that are not required for the
        current layer.
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
        """
        self.store = Gtk.ListStore(str, str, str, str, str, str, str, str)
        self.view = Gtk.TreeView(self.store)
        for x in range(8):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(str(x), renderer, text=x)
            column.set_alignment(0.5)
            column.set_expand(True)
            self.view.append_column(column)

        self.sw.add(self.view)
        self.dialog.show_all()

    def append_data(self, v):
        """
        Appends as many but a maximum of 8 columns it receives to the treestore
        that is shown in the parser dialog.
        """
        while len(v) < 8:
            v.append("")
        self.store.append([v[0], v[1], v[2], v[3], v[4], v[5], v[6], v[7]])

    def parse_file(self, start_line = 0):
        """
        Gathers the settings and parses the file. The results are pushed to
        the listview.
        """
        self.store.clear()
        f = open(self.file, "r")
        for key, line in enumerate(f):
            if key < start_line:
                continue
            else:
                string_list = re.split(r"[;,]", line)
                self.append_data(string_list)

    def on_spinbutton_start_line_value_changed(self, spinbutton):
        """
        Gets the new start line and calls the parse function again.
        """
        start_line = spinbutton.get_value()
        self.parse_file(start_line)

    def run(self):
        """
        Shows the dialog.
        """
        self.dialog.run()

    def on_file_parse_dialog_close(self, widget):
        """
        Triggered when the dialog is closed. Hides the dialog.
        """
        self.dialog.hide()

    def on_file_parse_dialog_destroy(self, widget):
        """
        Runs when the dialog is destroyed. Hides the dialog.
        """
        self.dialog.hide()

    def on_file_parse_dialog_response(self, widget, response):
        """
        Executes when a response is triggered.
        """
        self.dialog.hide()

    def on_button_parse_apply_clicked(self, button):
        """
        When apply is clicked this function appends all the data to the
        liststore of the active layer.
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
        self.tfpl_dic = {"0": "ukn", "1": "up", "2": "dn", "3": "dex", "4": "sin"}
        self.use_tfpl = self.checkbutton_tectonicsfpl.get_active()
        

        def iterate_over_planes(m, p, i):
            """
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
                if self.use_tfpl == True:
                    sense = self.tfpl_dic[m[p][cb_ln_sense][0:1]]
                else:
                    sense = str(m[p][cb_ln_sense])

            self.append_line(layer_store, dipdir, dip, sense)

        def iterate_over_faultplanes(m, p, i):
            """
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
                if self.use_tfpl == True:
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
        """
        Cancels the file parsing.
        """
        self.dialog.hide()
