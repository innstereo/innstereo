#!/usr/bin/python3

"""
This module contains the startup-function and the MainWindow-class.

The MainWindow-class sets up the GUI and controls all its signals. All other
modules and clases are controlled from this class. The startup-function creates
the first instance of the GUI when the program starts.
"""

from gi.repository import Gtk, Gdk, GdkPixbuf, Gio
from matplotlib.backends.backend_gtk3cairo import (FigureCanvasGTK3Cairo
                                                   as FigureCanvas)
from matplotlib.backends.backend_gtk3 import (NavigationToolbar2GTK3 
                                              as NavigationToolbar)
import mplstereonet
import numpy as np
import scipy.spatial as spatial
import webbrowser
import os
import csv
from matplotlib.lines import Line2D
import json

#Internal imports
from .dataview_classes import (PlaneDataView, LineDataView,
                              FaultPlaneDataView, SmallCircleDataView,
                              EigenVectorView)
from .layer_view import LayerTreeView
from .layer_types import (PlaneLayer, FaultPlaneLayer, LineLayer,
                         SmallCircleLayer, EigenVectorLayer)
from .dialog_windows import (AboutDialog, PrintDialog, StereonetProperties,
                            FileChooserParse, FileChooserExport,
                            FileChooserSave, FileChooserOpen)
from .layer_properties import LayerProperties
from .plot_control import PlotSettings
from .polar_axes import NorthPolarAxes
from .file_parser import FileParseDialog
from .rotation_dialog import RotationDialog


class MainWindow(object):

    """
    The MainWindow-class handles the properties and signals of the GUI.

    The class sets up the GUI and connects all signals. Most methods are
    for individual functions of the GUI.
    """

    def __init__(self, builder):
        """
        Initializes the main window and connects different functions.

        Initializes the GUI, connects all its sinals, and runs the
        Gtk-main-loop. An instance of the Gtk.Builder is required for init.
        An instance of the figure is created and added to the FigureCanvas.
        The global startup function enables the program to open another
        independent instance of the GUI.
        """
        global startup
        self.main_window = builder.get_object("main_window")
        self.sw_plot = builder.get_object("scrolledwindow1")
        self.sw_layer = builder.get_object("scrolledwindow2")
        self.sw_data = builder.get_object("scrolledwindow3")
        self.tb1 = builder.get_object("toolbar1")
        self.statbar = builder.get_object("statusbar1")
        self.plot_menu = builder.get_object("menu_plot_views")
        self.builder = builder

        #Set up default options class
        self.settings = PlotSettings()

        #Set up layer view and connect signals
        self.layer_store = Gtk.TreeStore(bool, GdkPixbuf.Pixbuf, str, object)
        self.layer_view = LayerTreeView(self.layer_store)
        self.sw_layer.add(self.layer_view)

        #Connect signals of layer view
        self.layer_view.renderer_name.connect("edited", self.layer_name_edited)
        self.layer_view.renderer_activate_layer.connect("toggled", 
            self.on_layer_toggled)
        self.layer_view.connect("row-activated", self.layer_row_activated)
        self.select = self.layer_view.get_selection()
        self.select.connect("changed", self.layer_selection_changed)
        self.draw_features = False
        self.layer_view.connect("drag-begin", self.drag_begin)
        self.layer_view.connect("drag-data-get", self.drag_data_get)
        self.layer_view.connect("drag-drop", self.drag_drop)
        self.layer_view.connect("drag-data-delete", self.drag_data_delete)
        self.layer_view.connect("drag-data-received", self.drag_data_received)
        self.layer_view.connect("drag-end", self.drag_end)

        #Set up the plot
        self.fig = self.settings.get_fig()
        self.canvas = FigureCanvas(self.fig)
        self.sw_plot.add_with_viewport(self.canvas)
        self.ax_stereo = self.settings.get_stereonet()
        self.inv = self.settings.get_inverse_transform()
        self.trans = self.settings.get_transform()
        self.view_mode = "stereonet"
        self.view_changed = False
        self.ax_rose = None

        #Set up the headerbar
        self.headerbar_setup()

        #Set up event-handlers
        self.canvas.mpl_connect('motion_notify_event', 
            self.update_cursor_position)
        self.canvas.mpl_connect('button_press_event',
            self.mpl_canvas_clicked)
        self.redraw_plot()
        self.main_window.show_all()

    def headerbar_setup(self):
        """
        Sets up the HeaderBar and the PopoverMenus.

        The Headerbar is set up in Pyton, while the PopoverMenus are parsed
        from XML files. Each PopoverMenu is connected to the appropriate button,
        and show/hide of the menu is set up.
        """
        self.hb = Gtk.HeaderBar()
        self.hb.set_show_close_button(True)
        self.hb.props.title = "InnStereo"
        self.main_window.set_titlebar(self.hb)

        def toggle_popover(button, popovermenu):
            """
            Toggles the respective popovermenu.
            """
            if popovermenu.get_visible():
                popovermenu.hide()
            else:
                popovermenu.show_all()

        #HeaderBar: Pack Start
        #######################################################################
        #Project: PopoverMenu
        button_project = Gtk.Button("Project")
        pom_project = self.builder.get_object("pom_project")
        pom_project.set_relative_to(button_project)
        button_project.connect("clicked", toggle_popover, pom_project)
        self.hb.pack_start(button_project)

        #Save: Button
        button_save = Gtk.Button("Save Image")
        button_save.connect("clicked", self.on_toolbutton_save_figure_clicked)
        self.hb.pack_start(button_save)

        #HeaderBar: Pack End
        #######################################################################
        button_settings = Gtk.Button()
        icon = Gio.ThemedIcon(name="format-justify-fill-symbolic")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        button_settings.add(image)
        self.hb.pack_end(button_settings)

        #Plot Properties: Button
        button_props = Gtk.Button()
        icon = Gio.ThemedIcon(name="document-properties-symbolic")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        button_props.add(image)
        button_props.connect("clicked", self.on_toolbutton_plot_properties_clicked)
        self.hb.pack_end(button_props)

        #View: PopoverMenu
        button_view = Gtk.Button("View")
        pom_view = self.builder.get_object("pom_view")
        pom_view.set_relative_to(button_view)
        button_view.connect("clicked", toggle_popover, pom_view)
        self.hb.pack_end(button_view)

        #Calculations: PopoverMenu
        button_calc = Gtk.Button("Calculate")
        pom_calc = self.builder.get_object("pom_calc")
        pom_calc.set_relative_to(button_calc)
        button_calc.connect("clicked", toggle_popover, pom_calc)
        self.hb.pack_end(button_calc)

        #Layer Style: Button
        button_style = Gtk.Button("Layer Style")
        button_style.connect("clicked", self.on_toolbutton_layer_properties_clicked)
        self.hb.pack_end(button_style)

    def drag_begin(self, treeview, context):
        """
        Drag begin signal of the layer view. Currently does nothing.

        This signal could be used to set up a e.g. drag icon.
        """
        pass

    def drag_data_get(self, treeview, context, selection, info, time):
        """
        Gets the data from the drag source. Serializes the data to JSON.

        Iterates over the draged layer and all its children. Serializes the
        path, properties and data. Encodes into JSON and sens it to the
        drag destinations.
        """
        tree_selection = treeview.get_selection()
        store, itr = tree_selection.get_selected_rows()
        model = self.layer_view.get_model()
        path = itr[0]
        path_str = str(path)
        itr = store.get_iter(path)

        copy = {}
        copy["filetype"] = "InnStereo layer 1.0"
        copy["layers"] = []

        def append_layer(lyr_obj, path_str, label):
            """
            Appends a layer to the serialization dictionary.

            Receives a store, iter and path_str. Appends the path, properties
            and data to the 'layers' list of the dictionary. For folders it
            appends the path, the folder-properties and an empty list (So that
            the destination can use iterators also for folders).
            """
            #The layer includes the layer and children as
            #[[path, properties, data],...]
            if lyr_obj is None:
                #No lyr_obj means that this is a folder
                folder_props = {"type": "folder", "label": label}
                copy["layers"].append([path_str, folder_props, []])
            else:
                properties = lyr_obj.get_properties()
                data = lyr_obj.return_data()
                copy["layers"].append([path_str, properties, data])

        def iterate_over_store(model, path, itr, start_path):
            """
            Iterates over the whole TreeStore and appends all draged layers.

            The function iterates over the whole TreeStore, but uses the
            path to identify the dragged layer and its children. Calls the
            append function on each these layers.
            """
            path_str = str(path)
            lyr_obj = store[itr][3]
            label = store[itr][2]
            if path_str.startswith(start_path) == True:
                append_layer(lyr_obj, path_str, label)

        self.layer_store.foreach(iterate_over_store, path_str)
        data = json.dumps(copy)
        selection.set(selection.get_target(), 8, data.encode())

    def drag_drop(self, treeview, context, selection, info, time):
        """
        Signal emitted when a layer is droped. Does nothing at the moment.
        """
        pass

    def drag_data_received(self, treeview, context, x, y, selection, info, time):
        """
        Called when data is received at the drop location. Moves the data.

        The received JSON is decoded and the validity checked. Then the layers
        are recreated and inserted at the drop location.
        """
        drop_info = self.layer_view.get_dest_row_at_pos(x, y)
        data = selection.get_data().decode()
        decoded = json.loads(data)

        filetype = decoded["filetype"]

        if filetype != "InnStereo layer 1.0":
            print("Not a valid layer")
            return

        def drop_layer(lyr_obj_new, lyr_dict, drop_iter, drop_position):
            if lyr_obj_new == None:
                lyr_pixbuf = self.settings.get_folder_icon()
                lyr_label = lyr_dict["label"]
            else:
                lyr_obj_new.set_properties(lyr_dict)
                lyr_pixbuf = lyr_obj_new.get_pixbuf()
                lyr_label = lyr_obj_new.get_label()

            if drop_lyr_obj is None:
                #0=Before, 1=After, 2=INTO_OR_BEFORE, 3=INTO_OR_AFTER
                if drop_position == Gtk.TreeViewDropPosition.BEFORE:
                    ins_itr = self.layer_store.insert_before(None, drop_iter,
                        [True, lyr_pixbuf, lyr_label, lyr_obj_new])
                elif drop_position == Gtk.TreeViewDropPosition.AFTER:
                    ins_itr = self.layer_store.insert_after(None, drop_iter,
                        [True, lyr_pixbuf, lyr_label, lyr_obj_new])
                else:
                    ins_itr = self.layer_store.insert_after(drop_iter, None,
                        [True, lyr_pixbuf, lyr_label, lyr_obj_new])
            else:
                if drop_position == Gtk.TreeViewDropPosition.BEFORE:
                    ins_itr = self.layer_store.insert_before(None, drop_iter,
                        [True, lyr_pixbuf, lyr_label, lyr_obj_new])
                else:
                    ins_itr = self.layer_store.insert_after(None, drop_iter,
                        [True, lyr_pixbuf, lyr_label, lyr_obj_new])
            return ins_itr

        def insert_layer(lyr_obj_new, lyr_dict, ins_iter):
            if lyr_obj_new == None:
                lyr_pixbuf = self.settings.get_folder_icon()
                lyr_label = lyr_dict["label"]
            else:
                lyr_obj_new.set_properties(lyr_dict)
                lyr_pixbuf = lyr_obj_new.get_pixbuf()
                lyr_label = lyr_obj_new.get_label()

            ins_itr = self.layer_store.insert_before(ins_iter, None,
                                    [True, lyr_pixbuf, lyr_label, lyr_obj_new])
            return ins_itr

        if drop_info is not None:
            #Insert the row at the drop position
            insert_rows = True
            drop_path, drop_position = drop_info[0], drop_info[1]
            drop_iter = self.layer_store.get_iter(drop_path)
            drop_row = self.layer_store[drop_iter]
            drop_lyr_obj = drop_row[3]

        else:
            #Append the row to the TreeStore
            insert_rows = False

        for key, layer in enumerate(decoded["layers"]):
            split_path = layer[0].split(":")
            lyr_dict = layer[1]
            lyr_data = layer[2]
            lyr_obj_new, lyr_store, lyr_view = self.create_layer(lyr_dict["type"])

            if lyr_obj_new is not None:
                lyr_obj_new.set_properties(lyr_dict)
                lyr_pixbuf = lyr_obj_new.get_pixbuf()
                lyr_label = lyr_obj_new.get_label()
            else:
                lyr_pixbuf = self.settings.get_folder_icon()
                lyr_label = lyr_dict["label"]

            if key == 0 and insert_rows == True:
                cutoff = len(layer[0].split(":"))
                ins_itr = drop_layer(lyr_obj_new, lyr_dict, drop_iter, drop_position)
                iter_dict = {0: ins_itr}
            elif key == 0 and insert_rows == False:


                cutoff = len(layer[0].split(":"))
                ins_itr = self.layer_store.append(None, [True, lyr_pixbuf, lyr_label, lyr_obj_new])
                iter_dict = {0: ins_itr}
            else:
                new_path = split_path[cutoff:]
                path_len = len(new_path)
                ins_itr = iter_dict[path_len-1]
                itr = insert_layer(lyr_obj_new, lyr_dict, ins_itr)
                iter_dict[path_len] = itr

            for f in lyr_data:
                if lyr_dict["type"] == "faultplane":
                    #Passing a list or tuple to the add feature function would be better.
                    self.add_feature(lyr_dict["type"], lyr_store, f[0], f[1], f[2], f[3], f[4])
                else:
                    self.add_feature(lyr_dict["type"], lyr_store, f[0], f[1], f[2])

            if insert_rows == False:
                self.redraw_plot()

        context.finish(True, True, time)

    def drag_end(self, treeview, context):
        """
        Signal when drag of a layer is complete. Redraws the plot.
        """
        self.redraw_plot()

    def drag_data_delete(self, treeview, context):
        """
        Signal is emitted when data is deleted. Does nothing at the moment.
        """
        pass

    def on_menuitem_stereo_activate(self, widget, *args):
        # pylint: disable=unused-argument
        """
        Switches to the stereonet-only view.

        Triggered from the menu bar. If the canvas is in a different view mode
        it switches to stereonet-only.
        """
        if self.view_mode is not "stereonet":
            self.view_changed = True
            self.view_mode = "stereonet"
            self.redraw_plot()

    def on_menuitem_stereo_rose_activate(self, widget, *args):
        # pylint: disable=unused-argument
        """
        Switches to the stereonet and rose-diagram view.

        Triggered from the menu bar. If the canvas is in a different view mode
        it will be switched to a combined stereonet and rose diagram view.
        """
        if self.view_mode is not "stereo-rose":
            self.view_changed = True
            self.view_mode = "stereo_rose"
            self.redraw_plot()

    def on_menuitem_rose_view_activate(self, widget, *args):
        # pylint: disable=unused-argument
        """
        Switches to the rose-diagram-only view.

        Triggered from the menu bar. If the canvas is in a different view mode
        it will be switched to a rose diagram only view.
        """
        if self.view_mode is not "rose":
            self.view_changed = True
            self.view_mode = "rose"
            self.redraw_plot()

    def on_menuitem_pt_view_activate(self, widget, *args):
        # pylint: disable=unused-argument
        """
        Switches to the paleostress view.

        Triggered from the menu bar. If the canvas is in a different view mode
        it switches to the PT-View.
        """
        if self.view_mode is not "pt":
            self.view_changed = True
            self.view_mode = "pt"
            self.redraw_plot()

    def change_night_mode(self):
        """
        Changes the night mode.

        Gets the current setting and applies it to the window.
        """
        state = self.settings.get_night_mode()
        Gtk.Settings.get_default().set_property("gtk-application-prefer-dark-theme", state)
        self.main_window.show_all()

    def on_toolbutton_eigenvector_clicked(self, widget, *args):
        # pylint: disable=unused-argument
        """
        Calculates the eigenvectors and eigenvalues of one or more layers.

        Triggered when the user calls the calculation. It checks if all the
        selected layers are either planes or linear-layers. If different
        layers are selected the calculation is aborted. A successful
        calculation adds a new eigenvector-layer.
        """
        selection = self.layer_view.get_selection()
        model, row_list = selection.get_selected_rows()
        values = []

        #Check if all selected layers are the same
        layers_equal = True
        layer_list = []
        for row in row_list:
            lyr_obj = model[row][3]

            if lyr_obj is None:
                return
            else:
                layer_list.append(lyr_obj.get_layer_type())
        for a in layer_list:
            for b in layer_list:
                if a is not b:
                    layers_equal = False

        if layers_equal == False:
            self.statbar.push(1, ("Please select only layers of the same type!"))
            return

        def evaluate_planes():
            total_strike = []
            total_dip = []
            for row in row_list:
                lyr_obj = model[row][3]
                strike, dipdir, dip = self.parse_planes(
                                                    lyr_obj.get_data_treestore())
                for x in strike:
                    total_strike.append(x)
                for y in dip:
                    total_dip.append(y)

            dip, dipdir, values = mplstereonet.eigenvectors(total_strike, total_dip)
            return dip, dipdir, values

        def evaluate_lines():
            total_dipdir = []
            total_dip = []
            for row in row_list:
                lyr_obj = model[row][3]
                dipdir, dip, sense = \
                                self.parse_lines(lyr_obj.get_data_treestore())
                for x in dipdir:
                    total_dipdir.append(x)
                for y in dip:
                    total_dip.append(y)

            dip, dipdir, values = mplstereonet.eigenvectors(total_dip,
                                                            total_dipdir,
                                                            measurement="lines")
            return dip, dipdir, values

        #Check how data should be interpreted:
        if layer_list[0] == "plane":
            dip, dipdir, values = evaluate_planes()
        elif layer_list[0] == "line":
            dip, dipdir, values = evaluate_lines()
        else:
            self.statbar.push(1, ("Please select only plane or line layers!"))
            return

        #Normalize to 1
        values = values/np.sum(values)

        store, new_lyr_obj = self.add_layer_dataset("eigenvector")
        self.add_eigenvector_feature(store, dipdir[0], dip[0], values[0])
        self.add_eigenvector_feature(store, dipdir[1], dip[1], values[1])
        self.add_eigenvector_feature(store, dipdir[2], dip[2], values[2])
        self.redraw_plot()

    def on_toolbutton_rotate_layer_clicked(self, toolbutton, *args):
        # pylint: disable=unused-argument
        """
        Open the data rotation dialog.

        If one or more layers are selected a instance of the data-rotation
        dialog is initialized and the selected rows are passed to it.
        """
        selection = self.layer_view.get_selection()
        model, row_list = selection.get_selected_rows()

        if len(row_list) == 0:
            self.statbar.push(1, ("Please select layers to rotate!"))
            return

        def parse_layers(model, path, itr, data, key):
            line = model[path]
            data[key][3].append([line[0], line[1], line[2]])

        data_rows = []
        for row in row_list:
            lyr_obj = model[row][3]
            data_rows.append(lyr_obj)

        rotate_dialog = RotationDialog(self.main_window, self.settings,
                                       data_rows, self.add_layer_dataset,
                                       self.add_feature, self.redraw_plot)
        rotate_dialog.run()

    def on_toolbutton_new_project_clicked(self, widget, *args):
        # pylint: disable=unused-argument
        """
        Opens a new and indenpendent window of the GUI.

        Triggered from the GUI. When the "new project"-button is pressed
        this function runs the startup function and creates a new and
        independent instance of the GUI.
        """
        startup()

    def on_menuitem_new_window_activate(self, widget):
        # pylint: disable=unused-argument
        """
        Opens a new and indenpendent window of the GUI.

        Triggered from the menu bar: "File -> New". Opens a new independent
        window by calling the global startup function.
        """
        startup()

    def on_toolbutton_poles_to_lines_clicked(self, widget, *args):
        # pylint: disable=unused-argument
        """
        Copies the poles of a plane-layer into a new line-layer.

        Checks if selected layers are planes or faultplanes. Copies the
        dip-direction - dip data into a line-dataset. If many layers are
        selected the data will be merged into one layer.
        """
        selection = self.layer_view.get_selection()
        model, row_list = selection.get_selected_rows()

        def iterate_over_data(model, path, itr, n):
            """
            Copies data to new layer.

            Receives a model, path and itr of a layer, plus the datastore
            of the new layer. Converts the plane orientation into a pole
            orientation and adds it to the new layer.
            """
            r = model[path]
            self.add_linear_feature(n, 180 + r[0], 90 - r[1])

        for row in row_list:
            lyr_obj = model[row][3]

            if lyr_obj is None:
                return
            else:
                layer_type = lyr_obj.get_layer_type()

            if layer_type == "line":
                return

        #n = new datastore
        n, new_lyr_obj = self.add_layer_dataset("line")

        for row in row_list:
            lyr_obj = model[row][3]
            datastore = lyr_obj.get_data_treestore()
            datastore.foreach(iterate_over_data, n)

        self.redraw_plot()

    def on_toolbutton_save_clicked(self, widget, *args):
        # pylint: disable=unused-argument
        """
        Triggered from the GUI. Saves the project.

        Iterates over all layers and stores the data in a dictionary. Passes
        the dictionary to the FileChooserSave dialog, which handles writing
        the file to the harddisk.
        """
        copy = {}
        copy["filetype"] = "InnStereo data file 1.0"
        copy["settings"] = self.settings.get_properties()
        copy["layers"] = []

        def append_layer(lyr_obj, path_str, label):
            """
            Appends a layer to the serialization dictionary.

            Receives a store, iter and path_str. Appends the path, properties
            and data to the 'layers' list of the dictionary. For folders it
            appends the path, the folder-properties and an empty list (So that
            the destination can use iterators also for folders).
            """
            #The layer includes the layer and children as
            #[[path, properties, data],...]
            if lyr_obj is None:
                #No lyr_obj means that this is a folder
                folder_props = {"type": "folder", "label": label}
                copy["layers"].append([path_str, folder_props, []])
            else:
                properties = lyr_obj.get_properties()
                data = lyr_obj.return_data()
                copy["layers"].append([path_str, properties, data])

        def iterate_over_store(model, path, itr):
            """
            Iterates over the whole TreeStore and appends all layers.

            The function iterates over the whole TreeStore and calls the append
            function on each layer.
            """
            path_str = str(path)
            lyr_obj = model[itr][3]
            label = model[itr][2]
            append_layer(lyr_obj, path_str, label)

        self.layer_store.foreach(iterate_over_store)
        dump = json.dumps(copy)
        dlg = FileChooserSave(self.main_window, dump)
        dlg.run()

    def on_toolbutton_open_clicked(self, toolbutton, *args):
        # pylint: disable=unused-argument
        """
        Triggered from the GUI. Opens a saved project.

        Runs the FileChooserOpen dialog. The dialog calls the open_project
        function if a file is opened.
        """
        dlg = FileChooserOpen(self.main_window, self.open_project)
        dlg.run()

    def open_project(self, project_file):
        """
        Opens a saved project. Adds all the saved layers to the current window

        The opened file is passed from the FileChooserOpen dialog. The file
        is read and then the json is parsed. The function then checks if
        the file is valid. Then each layer is added to the project. For each
        layer the saved properties are set and all the data rows are loaded.
        """
        with open(project_file, "r") as prj_file:
            read_data = prj_file.read()
        parse = json.loads(read_data)
        if parse["filetype"] != "InnStereo data file 1.0":
            print("Not a valid InnStereo data file")

        self.settings.set_properties(parse["settings"])

        def insert_layer(lyr_obj_new, lyr_dict, ins_iter):
            if lyr_obj_new == None:
                lyr_pixbuf = self.settings.get_folder_icon()
                lyr_label = lyr_dict["label"]
            else:
                lyr_obj_new.set_properties(lyr_dict)
                lyr_pixbuf = lyr_obj_new.get_pixbuf()
                lyr_label = lyr_obj_new.get_label()

            ins_itr = self.layer_store.insert_before(ins_iter, None,
                                    [True, lyr_pixbuf, lyr_label, lyr_obj_new])
            return ins_itr

        def create_and_insert(ins_itr, lyr_dict):
            lyr_obj_new, lyr_store, lyr_view = self.create_layer(lyr_dict["type"])
            ins_itr = insert_layer(lyr_obj_new, lyr_dict, ins_itr)
            if lyr_obj_new is not None:
                lyr_obj_new.set_properties(lyr_dict)
            return ins_itr, lyr_store

        iter_dict = {0: None}
        for layer in parse["layers"]:
            split_path = layer[0].split(":")
            path_len = len(split_path)
            lyr_dict = layer[1]
            features = layer[2]
            #The last path length is assigned to the dictionary
            #If the next layer has a longer path it will use the
            #previous entry as parent. It is not overwritten, which
            #produces a depth-first iteration.
            ins_itr = iter_dict[path_len-1]
            itr, lyr_store = create_and_insert(ins_itr, lyr_dict)
            iter_dict[path_len] = itr

            for f in features:
                if lyr_dict["type"] == "faultplane":
                #Passing a list or tuple to the add feature function would be better.
                    self.add_feature(lyr_dict["type"], lyr_store, f[0], f[1], f[2], f[3], f[4])
                else:
                    self.add_feature(lyr_dict["type"], lyr_store, f[0], f[1], f[2])

        self.redraw_plot()

    def on_toolbutton_show_table_clicked(self, widget):
        # pylint: disable=unused-argument
        """
        Opens dialog to view the data in a table.

        __!!__ Maybe implement sorting in this dialog?
        __!!__ Not implemented yet.
        """
        pass

    def on_toolbutton_delete_layer_clicked(self, widget):
        # pylint: disable=unused-argument
        """
        Deltes the currently selected layer(s).

        Triggered when the "remove layers" toolbutton is pressed. Deletes all
        selected layers.
        __!!__ Currently has no warning message. What happens to data?
        """
        selection = self.layer_view.get_selection()
        model, row_list = selection.get_selected_rows()

        for row in reversed(row_list):
            itr = model.get_iter(row)
            model.remove(itr)

        selection.unselect_all()
        self.redraw_plot()

    def on_toolbutton_plot_properties_clicked(self, widget):
        # pylint: disable=unused-argument
        """
        Opens the plot-properties dialog.

        Triggered when the toolbutton is pressed. Creates and instance of the
        StereonetProperties class, which is a Gtk DialogWindow and runs it.
        """
        plot_properties = StereonetProperties(self.settings, self.redraw_plot,
                                              self.main_window,
                                              self.change_night_mode)
        plot_properties.run()

    def on_toolbutton_print_figure_clicked(self, widget):
        # pylint: disable=unused-argument
        """
        Prints the figure.

        Triggered from the GUI. This function creates an instance of the
        GtkPrintUnixDialog and runs it.
        """
        pass
        #print_dialog = PrintDialog()
        #print_dialog.run()

    def on_toolbutton_save_figure_clicked(self, widget, *args):
        # pylint: disable=unused-argument
        """
        Opens a dialog to save the figure specified location and file-format.

        Opens the matplotlib dialog window that allows saving the current figure
        in a specified location, name and file format.
        """
        nav = NavigationToolbar(self.canvas, self.main_window)
        nav.save_figure()

    def layer_view_clicked(self, treeview, button):
        # pylint: disable=unused-argument
        """
        Unselects all layers if the layer-view is clicked.

        Called when one clicks with the mouse on the layer-treeview.
        Unselects all selected layers.
        """
        selection = self.layer_view.get_selection()
        selection.unselect_all()

    def on_toolbutton_draw_features_toggled(self, widget):
        # pylint: disable=unused-argument
        """
        Toggles if featues can be drawn by clicking on the canvas.

        Activated when the toggle button is pressed. When self.draw_features
        is True then clicking on the canvas with an active layer will draw
        a features at that point.
        """
        if self.draw_features is False:
            self.draw_features = True
        else:
            self.draw_features = False

    def on_toolbutton_best_plane_clicked(self, widget, *args):
        # pylint: disable=unused-argument
        """
        Finds the optimal plane for a set of linears.

        Iterates over all selected rows and collects the data. Finds the
        optimal plane that can be fitted to the data.
        """
        selection = self.layer_view.get_selection()
        model, row_list = selection.get_selected_rows()

        #Check if all selected layers are planes or faultplanes.
        only_linears = True
        for row in row_list:
            lyr_obj = model[row][3]
            if lyr_obj.get_layer_type() == "plane":
                only_linears = False

        if only_linears is False:
            return

        total_dipdir = []
        total_dip = []
        for row in row_list:
            lyr_obj = model[row][3]
            dipdir, dip, sense = self.parse_lines(
                                            lyr_obj.get_data_treestore())
            for x in dipdir:
                total_dipdir.append(x)
            for y in dip:
                total_dip.append(y)

        fit_strike, fit_dip = mplstereonet.fit_girdle(total_dip, total_dipdir,
                                measurement="lines")

        store, new_lyr_obj = self.add_layer_dataset("plane")
        self.add_planar_feature(store, fit_strike + 90, fit_dip)
        self.redraw_plot()

    def on_toolbutton_plane_intersect_clicked(self, widget, *args):
        # pylint: disable=unused-argument
        """
        Calculates the best fitting intersect for the selected planes.

        This method gathers all the dip-direction and dips of all selected
        layers. If linear layers are also selected nothing will be done.
        The best-fit intersection is added to the project as a new linear layer.
        """
        selection = self.layer_view.get_selection()
        model, row_list = selection.get_selected_rows()

        if len(row_list) == 0:
            return

        #Check if all selected layers are planes or faultplanes.
        only_planes = True
        for row in row_list:
            lyr_obj = model[row][3]
            if lyr_obj.get_layer_type() == "line":
                only_planes = False

        if only_planes is False:
            return

        total_dipdir = []
        total_dip = []

        #Iterate over layers and rows, gather poles
        for row in row_list:
            lyr_obj = model[row][3]
            strike, dipdir, dip = self.parse_planes(
                                            lyr_obj.get_data_treestore())
            for x in strike:
                total_dipdir.append(270 + x)
            for y in dip:
                total_dip.append(90 - y)
        
        self.ax_stereo.line(total_dip, total_dipdir)
        fit_strike, fit_dip = mplstereonet.fit_girdle(total_dip, total_dipdir,
                                measurement="lines")

        store, new_lyr_obj = self.add_layer_dataset("line")
        self.add_linear_feature(store, fit_strike + 270, 90 - fit_dip)
        self.redraw_plot()

    def on_toolbutton_linears_to_planes_clicked(self, toolbutton, *args):
        # pylint: disable=unused-argument
        """
        Finds the plane normal to the selected linears and adds them as planes.

        This method calculates the normal planes for all selected linear
        layers and adds them as a new plane dataset. This can be used to
        calculate the cross-section plane of a set of fold axis.
        """
        selection = self.layer_view.get_selection()
        model, row_list = selection.get_selected_rows()

        if len(row_list) == 0:
            return

        #Check if all selected layers are linear layers.
        only_lines = True
        for row in row_list:
            lyr_obj = model[row][3]
            if lyr_obj.get_layer_type() == "plane":
                only_lines = False
            elif lyr_obj.get_layer_type() == "faultplane":
                only_lines = False

        if only_lines is False:
            return

        store, new_lyr_obj = self.add_layer_dataset("plane")

        for row in row_list:
            lyr_obj = model[row][3]
            strike, dipdir, sense = self.parse_lines(
                                            lyr_obj.get_data_treestore())
            for strike, dipdir in zip(strike, dipdir):
                self.add_linear_feature(store, strike + 180, 90 - dipdir)

        self.redraw_plot()

    def on_toolbutton_mean_vector_clicked(self, toolbutton, *args):
        """
        Calculates the mean vector and adds it to the project.

        Parses line-layers and adds up all the values. then the mean vector
        is calculated and added to the project. The legend will show the
        dip-direction/dip of the mean vector and the coefficient of
        determination (r-value).
        """
        selection = self.layer_view.get_selection()
        model, row_list = selection.get_selected_rows()

        if len(row_list) == 0:
            return

        #Check if all selected layers are linear layers.
        only_lines = True
        for row in row_list:
            lyr_obj = model[row][3]
            if lyr_obj.get_layer_type() != "line":
                only_lines = False

        if only_lines is False:
            return

        total_dipdir = []
        total_dip = []
        for row in row_list:
            lyr_obj = model[row][3]
            store = lyr_obj.get_data_treestore()
            dipdir, dip, sense = self.parse_lines(store)
            for x, y in zip(dipdir, dip):
                total_dipdir.append(x)
                total_dip.append(y)

        lon, lat = mplstereonet.line(total_dip, total_dipdir)
        mean_vec, r_value = mplstereonet.stereonet_math.mean_vector(lon, lat)
        dipdir, dip = self.convert_lonlat_to_dipdir(mean_vec[0], mean_vec[1])

        new_store, new_lyr_obj = self.add_layer_dataset("eigenvector")
        new_lyr_obj.set_label("Mean Vector")
        self.add_linear_feature(new_store, dipdir, dip, r_value)

        self.redraw_plot()

    def convert_lonlat_to_dipdir(self, lon, lat):
        """
        Converts lat-lon data to dip-direction and dip.

        Expects a longitude and a latitude value. The measurment is forward
        transformed into stereonet-space. Then the azimut (dip-direction) and
        diping angle are calculated. Returns two values: dip-direction and dip.
        """
        #The longitude and latitude have to be forward-transformed to get
        #the corect azimuth angle
        xy = np.array([[lon, lat]])
        xy_trans = self.trans.transform(xy)
        x = float(xy_trans[0,0:1])
        y = float(xy_trans[0,1:2])
        alpha = np.arctan2(x, y)
        alpha_deg = np.degrees(alpha)
        if alpha_deg < 0:
            alpha_deg += 360

        #Longitude and Latitude don't need to be converted for rotation.
        #The correct dip is the array[1] value once the vector has been
        #rotated in north-south position.
        array = mplstereonet.stereonet_math._rotate(np.degrees(lon),
                                                    np.degrees(lat),
                                                    alpha_deg * (-1))
        gamma = float(array[1])
        gamma_deg = 90 - np.degrees(gamma)

        #If the longitude is larger or small than pi/2 the measurment lies
        #on the upper hemisphere and needs to be corrected.
        if lon > (np.pi / 2) or lon < (-np.pi / 2):
            alpha_deg = alpha_deg + 180

        return alpha_deg, gamma_deg

    def rotate_data(self, raxis, raxis_angle, dipdir, dip):
        """
        Rotates a measurment around a rotation axis a set number of degrees.

        Expects a rotation-axis, a rotation-angle, a dip-direction and a
        dip angle. The measurement is converted to latlot and then passed
        to the mplstereonet rotate function.
        """
        lonlat = mplstereonet.line(dip, dipdir)

        #Rotation around x-axis until rotation-axis azimuth is east-west
        rot1 = (90 - raxis[0])
        lon1 = np.degrees(lonlat[0])
        lat1 = np.degrees(lonlat[1])
        lon_rot1, lat_rot1 = mplstereonet.stereonet_math._rotate(lon1, lat1,
                                                      theta=rot1, axis="x")

        #Rotation around z-axis until rotation-axis dip is east-west
        rot2 = -(90 - raxis[1])
        lon2 = np.degrees(lon_rot1)
        lat2 = np.degrees(lat_rot1)
        lon_rot2, lat_rot2 = mplstereonet.stereonet_math._rotate(lon2, lat2,
                                                           theta=rot2, axis="z")
            
        #Rotate around the x-axis for the specified rotation:
        rot3 = raxis_angle
        lon3 = np.degrees(lon_rot2)
        lat3 = np.degrees(lat_rot2)
        lon_rot3, lat_rot3 = mplstereonet.stereonet_math._rotate(lon3, lat3,
                                                           theta=rot3, axis="x")

        #Undo the z-axis rotation
        rot4 = -rot2
        lon4 = np.degrees(lon_rot3)
        lat4 = np.degrees(lat_rot3)
        lon_rot4, lat_rot4 = mplstereonet.stereonet_math._rotate(lon4, lat4,
                                                           theta=rot4, axis="z")

        #Undo the x-axis rotation
        rot5 = -rot1
        lon5 = np.degrees(lon_rot4)
        lat5 = np.degrees(lat_rot4)
        lon_rot5, lat_rot5 = mplstereonet.stereonet_math._rotate(lon5, lat5,
                                                           theta=rot5, axis="x")
        dipdir5, dip5 = self.convert_lonlat_to_dipdir(lon_rot5, lat_rot5)
        return dipdir5, dip5

    def on_toolbutton_ptaxis_clicked(self, toolbutton, *args):
        """
        Calculates the PT-Axis of a faultplane, and add adds them to the project

        Triggered from the toolbar. One faultplane layer has to be selected.
        Iterates over the rows and calculates the p-, t, and b-axis for each
        of them.
        """
        selection = self.layer_view.get_selection()
        model, row_list = selection.get_selected_rows()

        if len(row_list) == 0:
            return

        if len(row_list) > 1:
            return

        row = row_list[0]
        lyr_obj = model[row][3]
        lyr_type = lyr_obj.get_layer_type()

        if lyr_type != "faultplane":
            return

        def iterate_over_data(model, path, itr, pbt_store):
            """
            Iterates over the faultplane and adds the pt-axis for each row.

            For each row the pole-linear-layer is calculated. The pole of
            that layer is the rotation axis and the b-axis. The linear is
            then rotated for the p-axis and t-axis.
            """
            drow = model[path]
            p_store = pbt_store[0]
            b_store = pbt_store[1]
            t_store = pbt_store[2]

            fit_strike, fit_dip = mplstereonet.fit_girdle(
                                    [float(drow[3]), 90 - float(drow[1])],
                                    [float(drow[2]), float(drow[0]) + 180],
                                    measurement="lines")
            #Plane between pole and linear
            self.ax_stereo.plane(fit_strike, fit_dip)

            #Rotation axis is pole of pole-linear-plane
            raxis = [fit_strike - 90, 90 - fit_dip]

            #B-Axis is rotation axis
            self.add_linear_feature(b_store, raxis[0], raxis[1])

            #Rotate 30° to P-axis
            if drow[4] == "dn" or drow[4] == "dex":
                rot = 30
            else:
                rot = -30
            p_dipdir, p_dip = self.rotate_data(raxis, rot, drow[2], drow[3])
            self.add_linear_feature(p_store, p_dipdir, p_dip)

            #Rotate 30°+120=150 to T-axis
            if drow[4] == "dn" or drow[4] == "dex":
                rot = -60
            else:
                rot = 60
            t_dipdir, t_dip = self.rotate_data(raxis, rot, drow[2], drow[3])
            self.add_linear_feature(t_store, t_dipdir, t_dip)

        p_store, p_lyr_obj = self.add_layer_dataset("line")
        p_lyr_obj.set_marker_fill("#ff0000")
        p_lyr_obj.set_marker_fill("#ff0000")
        p_lyr_obj.set_label("P-Axis")

        b_store, b_lyr_obj = self.add_layer_dataset("line")
        b_lyr_obj.set_marker_fill("#ffffff")
        b_lyr_obj.set_marker_style("s")
        b_lyr_obj.set_label("B-Axis")

        t_store, t_lyr_obj = self.add_layer_dataset("line")
        t_lyr_obj.set_marker_fill("#0000ff")
        t_lyr_obj.set_marker_style("^")
        t_lyr_obj.set_label("T-Axis")

        pbt_store = [p_store, b_store, t_store]

        lyr_store = lyr_obj.get_data_treestore()
        lyr_store.foreach(iterate_over_data, pbt_store)
        self.redraw_plot()

    def layer_row_activated(self, treeview, path, column):
        """
        Double clicking a layer, opens the layer-property dialog.

        Excecutes when a treeview row is double-clicked. This passes the
        treeview-object, the path (or row) as an integer and the
        TreeViewColumn-object to this function.
        """
        lyr_obj = self.layer_store[path][3]
        if lyr_obj is not None:
            layer_prop = LayerProperties(lyr_obj, self.redraw_plot, self.main_window)
            layer_prop.run()

    def on_toolbutton_layer_properties_clicked(self, toolbutton):
        """
        Triggered when the toolbutton for layer properties is pressed.

        Checks if only one layer is selected. If more or less layers are
        selected a warning is displayed in the statusbar.
        """
        selection = self.layer_view.get_selection()
        model, row_list = selection.get_selected_rows()

        if len(row_list) == 0:
            self.statbar.push(1, ("Please select a layer to customize."))
            return
        elif len(row_list) > 1:
            self.statbar.push(1, ("Please select only one layer to customize."))
            return

        row = row_list[0]
        lyr_obj = self.layer_store[row][3]
        layer_prop = LayerProperties(lyr_obj, self.redraw_plot, self.main_window)
        layer_prop.run()

    def layer_selection_changed(self, selection):
        """
        When the selection in the layer-view is changed to a layer containing
        data, then the data is displayed in the data-view. If more than one
        row is sected the data view is removed from the scrolled window.
        """
        model, row_list = selection.get_selected_rows()

        #If one row is selected show the data view, else don't show it
        if len(row_list) == 1:
            row = row_list[0]
            lyr_obj = model[row][3]
            child = self.sw_data.get_child()
            if lyr_obj is None:
                #If it has a child remove it
                if child is not None:
                    self.sw_data.remove(child)
            #Else: not a group layer
            else:
                #Get the treeview
                treeview_object = lyr_obj.get_data_treeview()
                #If there is a child remove it
                if child is not None:
                    self.sw_data.remove(child)
                #Add new treeview
                self.sw_data.add(treeview_object)
                data_treeview = lyr_obj.get_data_treeview()
                data_selection = data_treeview.get_selection()
                data_selection.unselect_all()
                self.main_window.show_all()
        else:
            child = self.sw_data.get_child()
            #If there is a child remove it
            if child is not None:
                self.sw_data.remove(child)
            #Add new treeview
            self.main_window.show_all()

        if self.settings.get_highlight() is True:
            self.redraw_plot()

    def on_layer_toggled(self, widget, path):
        # pylint: disable=unused-argument
        """
        Toggles the layer and redraws the plot.

        If the layer is toggled the bool field is switched between
        True (visible) and False (invisible). Then the plot is redrawn.
        """
        self.layer_store[path][0] = not self.layer_store[path][0]
        self.redraw_plot()

    def create_layer(self, lyr_type):
        """
        Creates a layer according to the passed layer type.

        Depending on the layer-type a different TreeStore, TreeView and layer
        object is created. For folders all of them are None. Returns the new
        layer object, a TreeStore and a TreeView.
        """
        if lyr_type == "plane":
            store = Gtk.ListStore(float, float, str)
            view = PlaneDataView(store, self.redraw_plot, self.add_feature,
                                 self.settings)
            lyr_obj_new = PlaneLayer(store, view)
        elif lyr_type == "faultplane":
            store = Gtk.ListStore(float, float, float, float, str)
            view = FaultPlaneDataView(store, self.redraw_plot, self.add_feature,
                                      self.settings)
            lyr_obj_new = FaultPlaneLayer(store, view)
        elif lyr_type == "line":
            store = Gtk.ListStore(float, float, str)
            view = LineDataView(store, self.redraw_plot, self.add_feature,
                                self.settings)
            lyr_obj_new = LineLayer(store, view)
        elif lyr_type == "smallcircle":
            store = Gtk.ListStore(float, float, float)
            view = SmallCircleDataView(store, self.redraw_plot, self.add_feature,
                                       self.settings)
            lyr_obj_new = SmallCircleLayer(store, view)
        elif lyr_type == "eigenvector":
            store = Gtk.ListStore(float, float, float)
            view = EigenVectorView(store, self.redraw_plot, self.add_feature,
                                   self.settings)
            lyr_obj_new = EigenVectorLayer(store, view)
        elif lyr_type == "folder":
            store = None
            view = None
            lyr_obj_new = None

        return lyr_obj_new, store, view

    def add_layer_dataset(self, layer_type):
        """
        Is called by the different "new layer" toolbuttons. If the number of
        selected rows are 0 or more than one, the layer is appended at the end.
        If just one row is selected, and the row is a group, then the new
        layer is created in that group. Otherwise it is added at the end of the
        same level as the selection.
        """
        store = None
        lyr_obj_new = None

        def add_layer(itr, layer_type):
            lyr_obj_new, store, view = self.create_layer(layer_type)
            view.set_layer_object(lyr_obj_new)
            pixbuf = lyr_obj_new.get_pixbuf()
            self.layer_store.append(itr,
                [True, pixbuf, lyr_obj_new.get_label(), lyr_obj_new])
            return store, lyr_obj_new

        selection = self.layer_view.get_selection()
        model, row_list = selection.get_selected_rows()

        rows = len(row_list)
        if rows == 0 or rows > 1:
            store, lyr_obj_new = add_layer(None, layer_type)
        else:
            #If selected item is group, add to group, else: add to level
            row = row_list[0]
            lyr_obj = model[row][3]
            selection_itr = model.get_iter(row_list[0])
            if lyr_obj is None:
                store, lyr_obj_new = add_layer(selection_itr, layer_type)
                self.layer_view.expand_row(row, True)
            else:
                parent_itr = model.iter_parent(selection_itr)
                store, lyr_obj_new = add_layer(parent_itr, layer_type)

        return store, lyr_obj_new

    def on_toolbutton_create_plane_dataset_clicked(self, widget):
        # pylint: disable=unused-argument
        """
        When the toolbutton "toolbutton_create_dataset" is pressed this function
        creates a new dataset in the currently active layer group.
        Each dataset has a corresponding data sheet.
        """
        self.add_layer_dataset("plane")

    def on_toolbutton_create_faultplane_dataset_clicked(self, widget):
        # pylint: disable=unused-argument
        """
        When the toolbutton "toolbutton_create_dataset" is pressed this function
        creates a new dataset in the currently active layer group.
        Each dataset has a corresponding data sheet.
        """
        self.add_layer_dataset("faultplane")

    def on_toolbutton_create_line_dataset_clicked(self, widget):
        # pylint: disable=unused-argument
        """
        Creates a new line data layer.
        """
        self.add_layer_dataset("line")

    def on_toolbutton_create_small_circle_clicked(self, widget):
        # pylint: disable=unused-argument
        """
        Creates a new small circle layer.
        """
        self.add_layer_dataset("smallcircle")

    def parse_planes(self, treestore, subset=None):
        """
        Parses planes and returns a list of strikes, dipdirs and dips.

        Parsing converts from dip direction to strikes.
        """
        strike = []
        dipdir = []
        dip = []
        for key, row in enumerate(treestore):
            if subset is not None and key not in subset:
                continue
            strike.append(float(row[0]) - 90)
            dipdir.append(float(row[0]))
            dip.append(float(row[1]))
        return strike, dipdir, dip

    def parse_faultplanes(self, treestore, subset=None):
        """
        Parses a faultplane treestore. Converts planes from dip-direction to
        strikes so they can be plotted.
        #lp_plane = linear-pole_plane (The great circles that connect the
        lineation with the pole of the faultplane. Used for Hoeppener-Plots.
        """
        strike = []
        plane_dir = []
        plane_dip = []
        line_dir = []
        line_dip = []
        sense = []
        line_sense_dir = []
        line_sense_dip = []
        lp_plane_dir = []
        lp_plane_dip = []
        for key, row in enumerate(treestore):
            if subset is not None and key not in subset:
                continue
            strike.append(float(row[0] - 90))
            plane_dir.append(float(row[0]))
            plane_dip.append(float(row[1]))
            line_dir.append(float(row[2]))
            line_dip.append(float(row[3]))
            sense.append(row[4])
            if row[4] == "up":
                line_sense_dir.append(float(row[2]) + 180)
                line_sense_dip.append(90 - float(row[3]))
            elif row[4] == "dn":
                line_sense_dir.append(float(row[2]))
                line_sense_dip.append(float(row[3]))
            fit_strike, fit_dip = mplstereonet.fit_girdle(
                                [float(row[3]), 90 - float(row[1])],
                                [float(row[2]), float(row[0]) + 180],
                                measurement="lines")
            lp_plane_dir.append(fit_strike)
            lp_plane_dip.append(fit_dip)
        return strike, plane_dir, plane_dip, line_dir, line_dip, sense, \
               line_sense_dir, line_sense_dip, lp_plane_dir, lp_plane_dip

    def parse_lines(self, treestore, subset=None):
        """
        Parses linear data with the 3 columns dip direction, dip and sense.
        Returns a python-list for each column.
        """
        line_dir = []
        line_dip = []
        sense = []
        for key, row in enumerate(treestore):
            if subset is not None and key not in subset:
                continue
            line_dir.append(float(row[0]))
            line_dip.append(float(row[1]))
            sense.append(row[2])
        return line_dir, line_dip, sense

    def parse_eigenvectors(self, treestore, subset=None):
        """
        Parses a eigenvector layer and returns a list of each column

        This method expect a TreeStore that stores the data of a layer. It
        iterates over the rows and adds each column to a list. It returns 3
        lists for line_dir, line_dip (the eigenvector) and values (the
        eigenvalue)
        """
        line_dir = []
        line_dip = []
        values = []
        for key, row in enumerate(treestore):
            if subset is not None and key not in subset:
                continue
            line_dir.append(float(row[0]))
            line_dip.append(float(row[1]))
            values.append(float(row[2]))
        return line_dir, line_dip, values

    def parse_smallcircles(self, treestore, subset=None):
        """
        Parses small circle data. Data has 3 columns: Dip direction, dip and
        opening angle.
        """
        line_dir = []
        line_dip = []
        angle = []
        for key, row in enumerate(treestore):
            if subset is not None and key not in subset:
                continue
            line_dir.append(float(row[0]))
            line_dip.append(float(row[1]))
            angle.append(float(row[2]))
        return line_dir, line_dip, angle

    def draw_plane(self, lyr_obj, dipdir, dip, highlight=False):
        """
        Function draws a great circle in the stereonet. It calls the formatting
        from the layer object.
        """
        num_data = len(dipdir)
        lbl = "{} ({})".format(lyr_obj.get_label(), num_data)

        if highlight is False:
            self.ax_stereo.plane(dipdir, dip, color=lyr_obj.get_line_color(),
                    label=lbl,
                    linewidth=lyr_obj.get_line_width(),
                    linestyle=lyr_obj.get_line_style(),
                    dash_capstyle=lyr_obj.get_capstyle(),
                    alpha=lyr_obj.get_line_alpha(), clip_on=False)
        else:
            self.ax_stereo.plane(dipdir, dip, color=lyr_obj.get_line_color(),
                    linewidth=lyr_obj.get_line_width() + 2,
                    linestyle=lyr_obj.get_line_style(),
                    dash_capstyle=lyr_obj.get_capstyle(),
                    alpha=lyr_obj.get_line_alpha(), clip_on=False)

    def draw_line(self, lyr_obj, dipdir, dip, highlight=False):
        """
        Function draws a linear element in the stereonet. It calls the
        formatting from the layer object.
        """
        num_data = len(dipdir)
        lbl = "{} ({})".format(lyr_obj.get_label(), num_data)

        if highlight is False:
        #ax.line takes dip first and then dipdir (as strike)
            self.ax_stereo.line(dip, dipdir, marker=lyr_obj.get_marker_style(),
                    markersize=lyr_obj.get_marker_size(),
                    color=lyr_obj.get_marker_fill(),
                    label=lbl,
                    markeredgewidth=lyr_obj.get_marker_edge_width(),
                    markeredgecolor=lyr_obj.get_marker_edge_color(),
                    alpha=lyr_obj.get_marker_alpha(), clip_on=False)
        else:
            self.ax_stereo.line(dip, dipdir, marker=lyr_obj.get_marker_style(),
                    markersize=lyr_obj.get_marker_size(),
                    color=lyr_obj.get_marker_fill(),
                    markeredgewidth=lyr_obj.get_marker_edge_width() + 2,
                    markeredgecolor=lyr_obj.get_marker_edge_color(),
                    alpha=lyr_obj.get_marker_alpha(), clip_on=False)

    def draw_eigenvector(self, lyr_obj, dipdir, dip, values, highlight=False):
        """
        Draws the eigenvectors as lines and adds the eigenvalues to the legend.

        This method is called from the redraw_plot method to draw a eigenvector
        layer. It expects a layer object and arrays for dip-direction, dips and
        values. The arrays are rounded and converted to strings for the legend.
        """
        dipdir = np.round(dipdir, 1).tolist()
        dip = np.round(dip, 1).tolist()
        values = np.round(values, 2).tolist()

        dipdir_str = []
        dip_str = []
        values_str = []

        for x in dipdir:
            dipdir_str.append(str(x).rjust(5, "0"))

        for y in dip:
            dip_str.append(str(y).rjust(4, "0"))

        for v in values:
            values_str.append(str(v))

        lbl = "{}   \n".format(lyr_obj.get_label())

        for key, value in enumerate(dipdir):
            lbl += "  {}/{}, {}\n".format(dipdir_str[key], dip_str[key],
                                          values_str[key])

        if highlight is False:
            #ax.line takes dip first and then dipdir (as strike)
            self.ax_stereo.line(dip, dipdir, marker=lyr_obj.get_marker_style(),
                    markersize=lyr_obj.get_marker_size(),
                    color=lyr_obj.get_marker_fill(),
                    label=lbl,
                    markeredgewidth=lyr_obj.get_marker_edge_width(),
                    markeredgecolor=lyr_obj.get_marker_edge_color(),
                    alpha=lyr_obj.get_marker_alpha(), clip_on=False)
        else:
            self.ax_stereo.line(dip, dipdir, marker=lyr_obj.get_marker_style(),
                    markersize=lyr_obj.get_marker_size() + 2,
                    color=lyr_obj.get_marker_fill(),
                    markeredgewidth=lyr_obj.get_marker_edge_width(),
                    markeredgecolor=lyr_obj.get_marker_edge_color(),
                    alpha=lyr_obj.get_marker_alpha(), clip_on=False)

    def draw_smallcircles(self, lyr_obj, dipdir, dip, angle, highlight=False):
        """
        Function draws small circles in the stereonet. It calls the formatting
        from the layer object.
        """
        if highlight is False:
        #ax.cone takes dip first and then dipdir!
        #facecolor needs to be "None" because there is a bug with which side to fill
            self.ax_stereo.cone(dip, dipdir, angle, facecolor="None",
                    color=lyr_obj.get_line_color(),
                    linewidth=lyr_obj.get_line_width(),
                    label=lyr_obj.get_label(),
                    linestyle=lyr_obj.get_line_style())
        else:
            self.ax_stereo.cone(dip, dipdir, angle, facecolor="None",
                    color=lyr_obj.get_line_color(),
                    linewidth=lyr_obj.get_line_width() + 2,
                    label=lyr_obj.get_label(),
                    linestyle=lyr_obj.get_line_style())

        num_data = len(dipdir)
        lbl = "{} ({})".format(lyr_obj.get_label(), num_data)

        handler = Line2D([], [], color=lyr_obj.get_line_color(),
                    linewidth=lyr_obj.get_line_width(),
                    linestyle=lyr_obj.get_line_style(),
                    dash_capstyle=lyr_obj.get_capstyle(),
                    alpha=lyr_obj.get_line_alpha())
        return handler, lbl

    def draw_poles(self, lyr_obj, dipdir, dip, highlight=False):
        """
        Function draws a plane pole in the stereonet. It calls the formatting
        from the layer object.
        """
        num_data = len(dipdir)
        lbl = "Poles of {} ({})".format(lyr_obj.get_label(), num_data)

        if highlight is False:
            self.ax_stereo.pole(dipdir, dip, marker=lyr_obj.get_pole_style(),
                    markersize=lyr_obj.get_pole_size(),
                    color=lyr_obj.get_pole_fill(),
                    label=lbl,
                    markeredgewidth=lyr_obj.get_pole_edge_width(),
                    markeredgecolor=lyr_obj.get_pole_edge_color(),
                    alpha=lyr_obj.get_pole_alpha(), clip_on=False)
        else:
            self.ax_stereo.pole(dipdir, dip, marker=lyr_obj.get_pole_style(),
                    markersize=lyr_obj.get_pole_size() + 2,
                    color=lyr_obj.get_pole_fill(),
                    markeredgewidth=lyr_obj.get_pole_edge_width(),
                    markeredgecolor=lyr_obj.get_pole_edge_color(),
                    alpha=lyr_obj.get_pole_alpha(), clip_on=False)

    def draw_contours(self, lyr_obj, dipdir, dips, measure_type):
        """
        MplStereonet accepts measurements as "poles" for planes and
        "lines" for linear measurements.
        """
        if len(dipdir) == 0:
            return None

        if lyr_obj.get_manual_range() == True:
            lower = lyr_obj.get_lower_limit()
            upper = lyr_obj.get_upper_limit()
            steps = lyr_obj.get_steps()
            cont_interval = np.linspace(lower, upper, num=steps)
        else:
            cont_interval = None

        #Implement hatches = (['-', '+', 'x', '\\', '*', 'o', 'O', '.'])
        if lyr_obj.get_draw_contour_fills() == True:
            cbar = self.ax_stereo.density_contourf(dipdir, dips,
                              measurement=measure_type,
                              method=lyr_obj.get_contour_method(),
                              gridsize=lyr_obj.get_contour_resolution(),
                              cmap=lyr_obj.get_colormap(),
                              sigma=lyr_obj.get_contour_sigma(),
                              levels=cont_interval)
        else:
            cbar = None

        if lyr_obj.get_draw_contour_lines() == True:
            if lyr_obj.get_use_line_color() == True:
                clines = self.ax_stereo.density_contour(dipdir, dips,
                                measurement=measure_type,
                                method = lyr_obj.get_contour_method(),
                                gridsize = lyr_obj.get_contour_resolution(),
                                sigma = lyr_obj.get_contour_sigma(),
                                colors = lyr_obj.get_contour_line_color(),
                                linewidths = lyr_obj.get_contour_line_width(),
                                linestyles = lyr_obj.get_contour_line_style(),
                                levels=cont_interval)
            else:
                clines = self.ax_stereo.density_contour(dipdir, dips,
                                measurement=measure_type,
                                method = lyr_obj.get_contour_method(),
                                gridsize = lyr_obj.get_contour_resolution(),
                                sigma = lyr_obj.get_contour_sigma(),
                                cmap = lyr_obj.get_colormap(),
                                linewidths = lyr_obj.get_contour_line_width(),
                                linestyles = lyr_obj.get_contour_line_style(),
                                levels=cont_interval)                

        if lyr_obj.get_draw_contour_labels() == True:
            if clines is not None:
                self.ax_stereo.clabel(clines,
                                fontsize = lyr_obj.get_contour_label_size())

        return cbar

    def draw_hoeppener(self, lyr_obj, plane_dir, plane_dip, line_dir,
                        line_dip, lp_plane_dir, lp_plane_dip, sense):
        """
        Receives data from a faultplane and draws a Hoeppener arrow.

        Triggered by the redraw_plot function.
        Receives a plane (direction and dip), linear (direction and dip), and
        the plane that connects them to each other (direction and dip). Finds
        the closest index to the pole on the pole-linear-plane and uses that
        index as the center of the arrow. The arrow connects the two points on
        the pole-linear-plane that lie f = 2 indexes in either direction. The
        length is corrected if it obviously crosses the stereonet (length > 1).
        Then the start and end direction is determined by the shear sense. If
        the datapoint has no shear sense no arrow is drawn. Unknown shear sense
        is just a line. The arrow direction is determined like this:
        -------------
        "up" (overthrust) Arrow should point away from equator.
        "dn" (downthrust) Arrow should point towards the equator.
        "sin" (sinistral strike-slip) Arrows should point left.
        "dex" (dextral strike-slip) Arrows should point right.
        __!!__ Still has a bug. Some orientations are wrong!
        """
        if len(line_dir) == 0:
            return

        def find_nearest_point(plane_stack, point):
            """
            Finds the closest index to the pole on the pole-linear-plane.

            The pole lies on the pole-linear plane. The index that is closest to
            this point is returned and further used as the center of the arrow.
            """
            tree = spatial.cKDTree(plane_stack)
            dist, index = tree.query(point)
            return index

        for k, x in enumerate(plane_dir):
            plane_lons, plane_lats = mplstereonet.plane(lp_plane_dir[k],
                                                        lp_plane_dip[k])
            line_lons, line_lats = mplstereonet.pole(plane_dir[k] - 90,
                                                     plane_dip[k])
            plane_stack = np.dstack([plane_lons.ravel(), plane_lats.ravel()])[0]
            point = np.array([line_lons, line_lats]).transpose()
            i = find_nearest_point(plane_stack, point)

            #This solution works well for short arrows. Longer arrows bypass
            #the pole point. If length of arrow is a concern this needs to be
            #redone in a different way.
            f = 2

            lon_start = plane_lons[i-f][0][0]
            lat_start = plane_lats[i-f][0][0]
            lon_end = plane_lons[i+f][0][0]
            lat_end = plane_lats[i+f][0][0]
            dlon = lon_end - lon_start
            dlat = lat_end - lat_start
            
            #If the arrow crosses the stereonet, the arrow is moved so long
            #until the closer point touches the edge of the stereonet
            c = 0
            while dlon > 1 or dlat > 1:
                c = c + 1
                if abs(lon_start) > abs(lon_end) or abs(lat_start) > (lat_end):
                    lon_start = plane_lons[i-f+c][0][0]
                    lat_start = plane_lats[i-f+c][0][0]
                    lon_end = plane_lons[i+f+c][0][0]
                    lat_end = plane_lats[i+f+c][0][0]
                else:
                    lon_start = plane_lons[i-f-c][0][0]
                    lat_start = plane_lats[i-f-c][0][0]
                    lon_end = plane_lons[i+f-c][0][0]
                    lat_end = plane_lats[i+f-c][0][0]
                
                dlon = lon_end - lon_start
                dlat = lat_end - lat_start

            #Correct the direction of the arrow
            if sense[k] == "up":
                if abs(lon_start) > abs(lon_end):
                    lon_start, lon_end = lon_end, lon_start
                    lat_start, lat_end = lat_end, lat_start

            elif sense[k] == "dn":
                if abs(lon_start) < abs(lon_end):
                    lon_start, lon_end = lon_end, lon_start
                    lat_start, lat_end = lat_end, lat_start

            elif sense[k] == "sin":
                if lon_start > lon_end:
                    lon_start, lon_end = lon_end, lon_start
                    lat_start, lat_end = lat_end, lat_start

            elif sense[k] == "dex":
                if lon_start < lon_end:
                    lon_start, lon_end = lon_end, lon_start
                    lat_start, lat_end = lat_end, lat_start

            #Draw line for "uk", nothing for "" and arrow for everything else
            #__!!__ The arrows direction might not be determined by
            #xy = start and xytext = end
            if sense[k] == "uk":
                self.ax_stereo.annotate("", xy = (lon_end, lat_end),
                                        xytext = (lon_start, lat_start),
                                        xycoords = "data",
                                        textcoords = "data",
                                        arrowprops = dict(arrowstyle = "-",
                                                      connectionstyle = "arc3"))
            elif sense[k] == "":
                pass
            else:
                self.ax_stereo.annotate("", xy = (lon_end, lat_end),
                                        xytext = (lon_start, lat_start),
                                        xycoords = "data",
                                        textcoords = "data",
                                        arrowprops = dict(arrowstyle = "->",
                                                      connectionstyle = "arc3"))

    def plot_layer(self, lyr_obj, subset=None, highlight=False):
        """
        Plots a certain layer or subset of layer.

        The method expect a layer-object which should be plotted. If only a
        subset should be plotted, a list containing the row number sof the
        subset has to be passed additionally. If the layer or subset should be
        highlighted the method additionally expect a boolean keyword argument:
        highlight = True. Each layer and subset is parsed and then passed to
        the respective drawing functions.
        """
        if lyr_obj == None:
            lyr_type = "group"
        else:
            lyr_type = lyr_obj.get_layer_type()
            store = lyr_obj.get_data_treestore()

        if lyr_type == "plane":
            strike, dipdir, dip = self.parse_planes(store, subset)

            if lyr_obj.get_draw_gcircles() == True:
                self.draw_plane(lyr_obj, strike, dip, highlight=highlight)

            if lyr_obj.get_draw_poles() == True:
                self.draw_poles(lyr_obj, strike, dip, highlight=highlight)

            self.draw_contours(lyr_obj, strike, dip, "poles")

            if self.ax_rose is not None:
                num_bins = 360 / lyr_obj.get_rose_spacing()
                bin_width = 2 * np.pi / num_bins
                dipdir = np.radians(dipdir)
                values, bin_edges = np.histogram(dipdir, num_bins,
                                                 range = (0, 2 * np.pi))
                self.ax_rose.bar(left = bin_edges[:-1], height = values,
                                     width = bin_width, alpha=0.5,
                                     color = lyr_obj.get_line_color(),
                                     edgecolor = lyr_obj.get_pole_edge_color(),
                                     bottom = lyr_obj.get_rose_bottom())

        elif lyr_type == "line":
            dipdir, dip, sense = self.parse_lines(store, subset)

            if lyr_obj.get_draw_linears() == True:
                self.draw_line(lyr_obj, dipdir, dip, highlight=highlight)

            self.draw_contours(lyr_obj, dip, dipdir, "lines")

            if self.ax_rose is not None:
                num_bins = 360 / lyr_obj.get_rose_spacing()
                bin_width = 2 * np.pi / num_bins
                dipdir = np.radians(dipdir)
                values, bin_edges = np.histogram(dipdir, num_bins,
                                                 range = (0, 2 * np.pi))

                self.ax_rose.bar(left = bin_edges[:-1], height = values,
                                     width = bin_width, alpha=0.5,
                                     color = lyr_obj.get_marker_fill(),
                                     edgecolor = lyr_obj.get_marker_edge_color(),
                                     bottom = lyr_obj.get_rose_bottom())

        elif lyr_type == "faultplane":
            strike, plane_dir, plane_dip, line_dir, line_dip, \
                sense, line_sense_dir, line_sense_dip, \
                lp_plane_dir, lp_plane_dip = (
                self.parse_faultplanes(store, subset))

            if lyr_obj.get_draw_gcircles() == True:
                self.draw_plane(lyr_obj, strike, plane_dip, highlight=highlight)
            if lyr_obj.get_draw_poles() == True:
                self.draw_poles(lyr_obj, strike, plane_dip, highlight=highlight)
            if lyr_obj.get_draw_linears() == True:
                self.draw_line(lyr_obj, line_dir, line_dip, highlight=highlight)
            if lyr_obj.get_draw_lp_plane() == True:
                self.ax_stereo.plane(lp_plane_dir, lp_plane_dip,
                                     linestyle="dotted",
                                     color="#000000", highlight=highlight)
            if lyr_obj.get_draw_hoeppener() == True:
               self.draw_hoeppener(lyr_obj, plane_dir, plane_dip,
                                   line_dir, line_dip, lp_plane_dir,
                                   lp_plane_dip, sense)


        elif lyr_type == "smallcircle":
            dipdir, dip, angle = self.parse_smallcircles(store, subset)
            handler, label = self.draw_smallcircles(lyr_obj, dipdir,
                                                    dip, angle,
                                                    highlight=highlight)
            self.sc_labels.append(label)
            self.sc_handlers.append(handler)

        elif lyr_type == "eigenvector":
            dipdir, dip, values = self.parse_lines(store, subset)
            if lyr_obj.get_draw_linears() == True:
                self.draw_eigenvector(lyr_obj, dipdir, dip, values,
                                      highlight=highlight)

            self.draw_contours(lyr_obj, dip, dipdir, "lines")

    def highlight_selection(self):
        """
        Gets the current selection and highlights it in the plot.

        If only a layer is selected the layer is passed to the redrawing
        function. If one or more data-rows are selected the row-numbers are
        stored in a subset list and passed with the layer to the redrawing
        function.
        """
        selection = self.layer_view.get_selection()
        model, row_list = selection.get_selected_rows()

        def highlight_layers():
            for row in row_list:
                lyr_obj = model[row][3]
                self.plot_layer(lyr_obj, highlight=True)

        def highlight_rows(lyr_obj, data_row_list):
            row_list_ints = []
            for row in data_row_list:
                row_list_ints.append(row.get_indices()[0])
            self.plot_layer(lyr_obj, row_list_ints, highlight=True)

        if len(row_list) == 1:
            row = row_list[0]
            lyr_obj = model[row][3]
            data_view = lyr_obj.get_data_treeview()
            data_selection = data_view.get_selection()
            data_model, data_row_list = data_selection.get_selected_rows()
            if len(data_row_list) > 0:
                highlight_rows(lyr_obj, data_row_list)
            else:
                highlight_layers()
        elif len(row_list) == 0:
            return
        else:
            highlight_layers()

    def redraw_plot(self, checkout_canvas = False):
        """
        This function is called after any changes to the datasets or when
        adding or deleting layer. The plot is cleared and then redrawn.
        layer[3] = layer object
        """
        if self.view_changed == True or checkout_canvas == True:
            self.view_changed = False
            if self.view_mode == "stereonet":
                self.inv = self.settings.get_inverse_transform()
                self.ax_stereo = self.settings.get_stereonet()
            elif self.view_mode == "stereo_rose":
                self.inv = self.settings.get_inverse_transform()
                self.ax_stereo, self.ax_rose = self.settings.get_stereo_rose()
            elif self.view_mode == "rose":
                self.inv = self.settings.get_inverse_transform()
                self.ax_rose = self.settings.get_rose_diagram()
            elif self.view_mode == "pt":
                self.inv = self.settings.get_inverse_transform()
                self.ax_stereo, self.ax_fluc, self.ax_mohr = (
                                            self.settings.get_pt_view())

        if self.view_mode == "stereonet":
            self.ax_stereo.cla()
        elif self.view_mode == "stereo_rose":
            self.ax_rose.cla()
            self.ax_stereo.cla()
        elif self.view_mode == "rose":
            self.ax_rose.cla()
        elif self.view_mode == "pt":
            self.ax_stereo.cla()
            self.ax_fluc.cla()
            self.ax_mohr.cla()

        if self.settings.get_draw_grid_state() == True:
            self.ax_stereo.grid(linestyle = self.settings.get_grid_linestyle(),
                                color = self.settings.get_grid_color(),
                                linewidth = self.settings.get_grid_width())

        if self.settings.get_show_cross() == True:
            self.ax_stereo.annotate("", xy = (-0.03, 0),
                                    xytext = (0.03, 0),
                                    xycoords = "data",
                                    arrowprops = dict(arrowstyle = "-",
                                                      connectionstyle = "arc3"))
            self.ax_stereo.annotate("", xy = (0, -0.03),
                                    xytext = (0, 0.03),
                                    xycoords = "data",
                                    arrowprops = dict(arrowstyle = "-",
                                                      connectionstyle = "arc3"))

        if self.settings.get_show_north() == True:
            self.ax_stereo.set_azimuth_ticks([0], labels=['N'])

        if self.settings.get_highlight() is True:
            self.highlight_selection()

        deselected = []
        def iterate_over_rows(model, path, itr):
            lyr_obj = model[path][3]
            if lyr_obj is not None:
                layer_type = lyr_obj.get_layer_type()
                model[path][2] = lyr_obj.get_label()
                model[path][1] = lyr_obj.get_pixbuf()
            else:
                layer_type = "group"

            if model[path][0] == False:
                deselected.append(str(path))
                return
            
            draw = True
            for d in deselected:
                if str(path).startswith(d) == True:
                    draw = False

            if draw == False:
                return

            self.plot_layer(lyr_obj)

        self.sc_labels = []
        self.sc_handlers = []
        self.layer_store.foreach(iterate_over_rows)

        if self.settings.get_draw_legend() == True:
            handles, labels = self.ax_stereo.get_legend_handles_labels()
            newLabels, newHandles = [], []
            for handle, label in zip(handles, labels):
                if label not in newLabels:
                    newLabels.append(label)
                    newHandles.append(handle)

            for handle, label in zip(self.sc_handlers, self.sc_labels):
                if label not in newLabels:
                    newLabels.append(label)
                    newHandles.append(handle)

            if len(newHandles) is not 0:
                leg = self.ax_stereo.legend(newHandles, newLabels,
                                      bbox_to_anchor=(1.5, 1.1), borderpad=1,
                                      numpoints=1)
                leg.draggable(state=True)
        self.canvas.draw()

    def on_toolbutton_create_group_layer_clicked(self, widget):
        """
        When the toolbutton "toolbutton_create_layer" is pressed this function
        calls the "add_layer"-function of the TreeStore. The called function
        creates a new layer-group at the end of the view.
        """
        selection = self.layer_view.get_selection()
        model, row_list = selection.get_selected_rows()
        same_depth = True

        def check_same_depth(rows):
            return rows[1:] == rows[:-1]

        if len(row_list) > 0:
            first_path = row_list[0]
            first_itr = model.get_iter(first_path)

        #If no row is selected then the group is added to the end of the view
        if len(row_list) == 0:
            model.append(None,
                [True, self.settings.get_folder_icon(), "Layer Group", None])
        else:
            depth_list = []
            for row in row_list:
                itr = model.get_iter(row)
                depth_list.append(self.layer_store.iter_depth(itr))
                if check_same_depth(depth_list) == False:
                    same_depth = False
                    print("Selection is not on the same depth")
                    selection.unselect_all()
                    return

        def move_rows(parent_itr, itr):
            """
            Adds each row to the parent iter. First call is new group and
            first row that was selected.
            Checks if it has children. If yes, it start a recursive loop.
            """
            #ov = old values
            ov = model[itr]
            new_itr = model.append(parent_itr, [ov[0], ov[1], ov[2], ov[3]])
            children_left = model.iter_has_child(itr)
            while children_left == True:
                child = model.iter_children(itr)
                move_rows(new_itr, child)
                model.remove(child)
                children_left = model.iter_has_child(itr)

        if same_depth == True and len(row_list) > 0:
            selection_itr = model.get_iter(row_list[0])
            parent_itr = model.iter_parent(selection_itr)
            new_group_itr = model.insert_before(parent_itr, selection_itr,
                         [True, self.settings.get_folder_icon(),
                         "Layer group", None])
            selection = self.layer_view.get_selection()
            model, row_list = selection.get_selected_rows()
            for row in reversed(row_list):
                k = model[row]
                itr = model.get_iter(row)
                move_rows(new_group_itr, itr)
                model.remove(itr)

            new_path = model.get_path(new_group_itr)
            self.layer_view.expand_row(new_path, True)

    def layer_name_edited(self, widget, path, new_label):
        """
        When the layer name is edited this function passes the new label to the
        TreeStore along with the correct path.
        """
        self.layer_store[path][2] = new_label
        lyr_obj = self.layer_store[path][3]

        if lyr_obj is not None:
            lyr_obj.set_label(new_label)

        self.redraw_plot()

    def on_menuitem_about_activate(self, widget):
        """
        Triggered when the menuitem "about" is pressed. Creates an instance
        of the AboutDialog class and calls the function "run" within that class
        to show the dialog.
        """
        about = AboutDialog(self.main_window)
        about.run()

    def on_menuitem_quit_activate(self, widget, *args):
        """
        Triggered when the main window is closed from the menu. Terminates the
        Gtk main loop.
        """
        Gtk.main_quit()

    def on_main_window_destroy(self, widget):
        """
        Triggered when the main window is closed with the x-Button.
        Terminates the Gtk main loop
        """
        Gtk.main_quit()

    def on_toolbutton_remove_feature_clicked(self, widget):
        """
        Triggered when the toolbutton "remove feature" is clicked. Removes all
        the selected data rows from the currently active layer.
        """
        selection = self.layer_view.get_selection()
        model, row_list = selection.get_selected_rows()

        if len(row_list) == 1:
            row = row_list[0]
            lyr_obj = model[row][3]
            data_treeview = lyr_obj.get_data_treeview()
            data_treestore = lyr_obj.get_data_treestore()
            data_selection = data_treeview.get_selection()
            data_model, data_row_list = data_selection.get_selected_rows()
            treeiter_list = []

            for p in reversed(data_row_list):
                itr = data_model.get_iter(p)
                data_treestore.remove(itr)

        self.redraw_plot()

    def convert_xy_to_dirdip(self, event):
        """
        Converts xy-coordinates of a matplotlib-event into dip-direction/dip
        by using the inverse transformation of mplstereonet. Returns floats in
        degree.
        """
        alpha = np.arctan2(event.xdata, event.ydata)
        alpha_deg = np.degrees(alpha)
        if alpha_deg < 0:
            alpha_deg += 360

        xy = np.array([[event.xdata, event.ydata]])
        xy_trans = self.inv.transform(xy)

        x = float(xy_trans[0,0:1])
        y = float(xy_trans[0,1:2])

        array = mplstereonet.stereonet_math._rotate(np.degrees(x),
                    np.degrees(y), (-1)*alpha_deg)

        gamma = float(array[1])
        gamma_deg = 90 - np.degrees(gamma)
        return alpha_deg, gamma_deg

    def add_planar_feature(self, datastore, dip_direct=0, dip=0, sense=""):
        """
        Adds a planar feature row. Defaults to an empty row unless a dip
        direction and dip are given.
        """
        while dip_direct > 360:
            dip_direct = dip_direct - 360
        while dip_direct < 0:
            dip_direct = dip_direct + 360
        while dip > 90:
            dip = dip - 90
        while dip < 0:
            dip = dip + 90
            
        itr = datastore.append([dip_direct, dip, sense])
        return itr

    def add_linear_feature(self, datastore, dip_direct=0, dip=0, sense=""):
        """
        Adds a linear feature row. Defaults to an empty row unless a dip
        direction and dip are given.
        """
        while dip_direct > 360:
            dip_direct = dip_direct - 360
        while dip_direct < 0:
            dip_direct = dip_direct + 360
        while dip > 90:
            dip = dip - 90
        while dip < 0:
            dip = dip + 90

        itr = datastore.append([dip_direct, dip, sense])
        return itr

    def add_eigenvector_feature(self, datastore, dip_direct=0, dip=0, value=0):
        """
        Adds an eigenvector feature.

        Checks if the values lie in the normal range of degrees. Then the
        row is appended to the treestore that is passed to the method.
        """
        while dip_direct > 360:
            dip_direct = dip_direct - 360
        while dip_direct < 0:
            dip_direct = dip_direct + 360
        while dip > 90:
            dip = dip - 90
        while dip < 0:
            dip = dip + 90

        itr = datastore.append([dip_direct, dip, value])
        return itr

    def add_faultplane_feature(self, datastore, dip_direct = 0, dip = 0,
                               ldip_direct = 0, ldip = 0, sense = ""):
        """
        Adds a faultplane feature at the 
        """
        itr = datastore.append([dip_direct, dip, ldip_direct, ldip, sense])
        return itr

    def add_smallcircle_feature(self, datastore, dip_direct=0, dip=0,
                                angle=10):
        """
        Adds a small circle feature row. Defaults to an empty row unless a dip
        direction and dip are given.
        """
        itr = datastore.append([dip_direct, dip, angle])
        return itr

    def add_feature(self, layer_type, store, *args):
        """
        Adds a feature to a layer.

        Exepects a layer-type and a datastore. Additional arguments are passed
        to the specific function (e.g. dipdirection or dip)
        """
        if layer_type == "plane":
            itr = self.add_planar_feature(store, *args)
        if layer_type == "line":
            itr = self.add_linear_feature(store, *args)
        if layer_type == "faultplane":
            itr = self.add_faultplane_feature(store, *args)
        if layer_type == "smallcircle":
            itr = self.add_smallcircle_feature(store, *args)

    def on_toolbutton_add_feature_clicked(self, widget):
        """
        Adds an empty row to the currently selected data layer.

        The newly created is selected for easier editing.
        """
        selection = self.layer_view.get_selection()
        model, row_list = selection.get_selected_rows()

        if len(row_list) == 1:
            layer = row_list[0]
            current = model[layer][3]
            data_treestore = current.get_data_treestore()
            if data_treestore is not None:
                layer_type = current.get_layer_type()
                if layer_type == "plane":
                    itr = self.add_planar_feature(data_treestore)
                elif layer_type == "line":
                    itr = self.add_linear_feature(data_treestore)
                elif layer_type == "faultplane":
                    itr = self.add_faultplane_feature(data_treestore)
                elif layer_type == "smallcircle":
                    itr = self.add_smallcircle_feature(data_treestore)
                elif layer_type == "eigenvector":
                    itr = self.add_eigenvector_feature(data_treestore)

            data_treeview = model[layer][3].get_data_treeview()
            data_selection = data_treeview.get_selection()
            data_selection.unselect_all()
            data_selection.select_iter(itr)

    def mpl_canvas_clicked(self, event):
        """
        If the edit mode is off, clicking anywhere on the mpl canvas should
        deselect the layer treeview.
        If the edit mode is on the layer should stay selected and each
        click should draw a feature.
        """
        selection = self.layer_view.get_selection()
        if event.inaxes is not None:
            if self.draw_features == False:
                selection.unselect_all()
                return

            selection = self.layer_view.get_selection()
            model, row_list = selection.get_selected_rows()

            if len(row_list) == 1:
                if event.inaxes is not None:
                    alpha_deg, gamma_deg = self.convert_xy_to_dirdip(event)
            else:
                selection.unselect_all()
                return
            
            layer = row_list[0]
            lyr_obj = model[layer][3]
            if lyr_obj == None:
                #Layer is a layer-group
                return
            data_treestore = lyr_obj.get_data_treestore()

            if data_treestore is not None:
                layer_type = lyr_obj.get_layer_type()
                if layer_type == "plane":
                    self.add_planar_feature(data_treestore, alpha_deg,
                                            gamma_deg)
                if layer_type == "line":
                    self.add_linear_feature(data_treestore, alpha_deg,
                                            gamma_deg)
                if layer_type == "faultplane":
                    self.add_faultplane_feature(data_treestore, alpha_deg,
                                            gamma_deg)
                if layer_type == "smallcircle":
                    self.add_smallcircle_feature(data_treestore, alpha_deg,
                                            gamma_deg)
                self.redraw_plot()

    def update_cursor_position(self, event):
        """
        When the mouse cursor hovers inside the plot, the position of the
        event is pushed to the statusbar at the bottom of the GUI.
        """
        if event.inaxes is not None:
            alpha_deg, gamma_deg = self.convert_xy_to_dirdip(event)

            alpha_deg = int(alpha_deg)
            gamma_deg = int(gamma_deg)

            #Ensure 000/00 formatting
            alpha_deg = str(alpha_deg).rjust(3, "0")
            gamma_deg = str(gamma_deg).rjust(2, "0")

            self.statbar.push(1, ("{0} / {1}".format(alpha_deg, gamma_deg)))
        else:
            self.statbar.push(1, (""))

    def on_toolbutton_file_parse_clicked(self, toolbutton):
        """
        Triggered from the GUI. Opens the filechooserdialog for parsing text
        files.
        """
        selection = self.layer_view.get_selection()
        model, row_list = selection.get_selected_rows()

        if len(row_list) == 1:
            fc = FileChooserParse(self.run_file_parser, self.main_window)
            fc.run()

        elif len(row_list) == 0:
            self.statbar.push(1, ("Please select a layer to add data to."))
            self.canvas.draw()

        elif len(row_list) > 1:
            self.statbar.push(1,
                              ("Please select only one layer to add data to."))
            self.canvas.draw()

    def run_file_parser(self, text_file):
        """
        Triggered when a file is opend from the filechooserdialog for parsing
        files. Passes the file to the file parsing dialog.
        """
        selection = self.layer_view.get_selection()
        model, row_list = selection.get_selected_rows()

        if len(row_list) == 1:
            row = row_list[0]
            lyr_obj = model[row][3]
            fp = FileParseDialog(text_file, lyr_obj, self.redraw_plot,
                                 self.add_planar_feature,
                                 self.add_linear_feature,
                                 self.add_faultplane_feature, self.main_window)
            fp.run()

    def on_toolbutton_export_clicked(self, toolbutton):
        # pylint: disable=unused-argument
        """
        Runs the FileChooserExport dialog.

        Triggered when user clicks on the toolbutton_export. Creates an instance
        of the FileChooserExport class and runs the dialog. Checks if the user
        has selected a layer first.
        """
        selection = self.layer_view.get_selection()
        model, row_list = selection.get_selected_rows()

        if len(row_list) == 1:
            self.redraw_plot()
            exportdialog = FileChooserExport(self.export_data, self.main_window)
            exportdialog.run()

        elif len(row_list) == 0:
            self.statbar.push(1, ("Please select a layer to export."))
            self.canvas.draw()

        elif len(row_list) > 1:
            self.statbar.push(1, ("Please select only one layer to export."))
            self.canvas.draw()

    def export_data(self, save_location):
        """
        Exports data to a location that is passes by the FileExportDialog.

        This method receives a save_location from the FileExportDialog class.
        A CSV file is created at that location. Depending on the layer type a
        different header is written to the file and it then iterates over
        all rows.
        """
        selection = self.layer_view.get_selection()
        model, row_list = selection.get_selected_rows()

        def iterate_over_planes(model, path, itr):
            r = model[path]
            writer.writerow({"dip-direction": r[0], "dip": r[1],
                             "stratigraphy": r[2]})

        def iterate_over_linears(model, path, itr):
            r = model[path]
            writer.writerow({"dip-direction": r[0], "dip": r[1],
                             "sense": r[2]})

        def iterate_over_faultplanes(model, path, itr):
            r = model[path]
            writer.writerow({"plane-dip-direction": r[0],
                             "plane-dip": r[1],
                             "linear-dip-direction": r[2],
                             "linear-dip": r[3],
                             "linear-sense": r[4]})

        def iterate_over_smallcircles(model, path, itr):
            r = model[path]
            writer.writerow({"dip-direction": r[0],
                             "dip": r[1],
                             "opening-angle": r[2]})

        row = row_list[0]
        lyr_obj = model[row][3]
        data_obj = lyr_obj.get_data_treestore()

        with open(save_location, "w", newline="") as csvfile:
            lyr_type = lyr_obj.get_layer_type()
            if lyr_type == "plane":
                fieldnames = ["dip-direction", "dip", "stratigraphy"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                data_obj.foreach(iterate_over_planes)
            elif lyr_type == "line":
                fieldnames = ["dip-direction", "dip", "sense"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                data_obj.foreach(iterate_over_linears)
            elif lyr_type == "faultplane":
                fieldnames = ["plane-dip-direction", "plane-dip",
                              "linear-dip-direction", "linear-dip",
                              "linear-sense"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                data_obj.foreach(iterate_over_faultplanes)
            elif lyr_type == "smallcircle":
                fieldnames = ["dip-direction", "dip", "opening-angle"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                data_obj.foreach(iterate_over_smallcircles)

    def on_menuitem_online_help_activate(self, menuitem):
        # pylint: disable=unused-argument
        """
        This menuitem opens a new browser tab with the online help.

        Triggered when the user clicks "Help -> View Online Help" in the
        MenuBar.
        """
        webbrowser.open_new_tab(
                        "http://innstereo.readthedocs.org")

    def on_menuitem_website_activate(self, menuitem):
        # pylint: disable=unused-argument
        """
        This menuitem opens a new browser tab with the website of InnStereo.

        Triggered when the user clicks "Help -> Visit the Website" in the
        MenuBar.
        """
        webbrowser.open_new_tab(
                "http://innstereo.github.io/")

    def on_menuitem_report_bug_activate(self, menuitem):
        # pylint: disable=unused-argument
        """
        This menuitem opens a new browser tab with the bug tracker.

        Triggered when the user clicks "Help -> Report a Bug" in the
        MenuBar.
        """
        webbrowser.open_new_tab(
            "https://github.com/tobias47n9e/innstereo/issues")


def startup():
    """
    Starts the GUI and the application main-loop.

    Initializes an instance of the Gtk.Builder and loads the GUI from the
    ".glade" file. Then it initializes the main window and starts the Gtk.main
    loop. This function is also passed to the window, so it can open up new
    instances of the program.
    """
    builder = Gtk.Builder()

    script_dir = os.path.dirname(__file__)
    rel_path = "gui_layout.glade"
    abs_path = os.path.join(script_dir, rel_path)

    objects = builder.add_objects_from_file(abs_path,
         ("main_window", "image_new_plane", "image_new_faultplane",
         "image_new_line", "image_new_fold", "image_plane_intersect",
         "image_best_fitting_plane", "layer_right_click_menu",
         "image_create_small_circle", "menu_plot_views", "image_eigenvector",
         "poles_to_lines", "image_linears_to_planes", "image_rotate",
         "image_pt_axis", "image_mean_vector"))

    abs_path_ui1 =  os.path.join(script_dir, "ui/popovermenu_project.xml")
    objects = builder.add_from_file(abs_path_ui1)

    abs_path_ui2 =  os.path.join(script_dir, "ui/popovermenu_calc.xml")
    objects = builder.add_from_file(abs_path_ui2)

    abs_path_ui3 =  os.path.join(script_dir, "ui/popovermenu_view.xml")
    objects = builder.add_from_file(abs_path_ui3)

    gui_instance = MainWindow(builder)
    builder.connect_signals(gui_instance)
    Gtk.main()

if __name__ == "__main__":
    startup()
