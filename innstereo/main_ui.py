#!/usr/bin/python3

"""
This module contains the startup-function and the MainWindow-class.

The MainWindow-class sets up the GUI and controls all its signals. All other
modules and clases are controlled from this class. The startup-function creates
the first instance of the GUI when the program starts.
"""

from gi.repository import Gtk, GdkPixbuf
from matplotlib.backends.backend_gtk3cairo import (FigureCanvasGTK3Cairo
                                                   as FigureCanvas)
from matplotlib.backends.backend_gtk3 import (NavigationToolbar2GTK3 
                                              as NavigationToolbar)
import mplstereonet
import numpy as np
import scipy
import webbrowser
import os
import csv

#Internal imports
from .dataview_classes import (PlaneDataView, LineDataView,
                              FaultPlaneDataView, SmallCircleDataView)
from .layer_view import LayerTreeView
from .layer_types import PlaneLayer, FaultPlaneLayer, LineLayer, SmallCircleLayer
from .dialog_windows import (AboutDialog, PrintDialog, StereonetProperties,
                            FileChooserParse, FileChooserExport)
from .layer_properties import LayerProperties
from .plot_control import PlotSettings
from .polar_axes import NorthPolarAxes
from .file_parser import FileParseDialog


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

        context = self.tb1.get_style_context()
        context.add_class(Gtk.STYLE_CLASS_PRIMARY_TOOLBAR)

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

        #Set up event-handlers
        self.canvas.mpl_connect('motion_notify_event', 
            self.update_cursor_position)
        self.canvas.mpl_connect('button_press_event',
            self.mpl_canvas_clicked)
        self.redraw_plot()
        self.main_window.show_all()

    def on_menuitem_stereo_activate(self, widget):
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

    def on_menuitem_stereo_rose_activate(self, widget):
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

    def on_menuitem_rose_view_activate(self, widget):
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

    def on_menuitem_pt_view_activate(self, widget):
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

    def on_toolbutton_eigenvector_clicked(self, widget):
        # pylint: disable=unused-argument
        """
        Calculates the eigenvectors and eigenvalues of one or more layers.

        __!!__Implemented in mplstereonet now, change this function!
        """
        selection = self.layer_view.get_selection()
        model, row_list = selection.get_selected_rows()

        total_dipdir = []
        total_dip = []
        for row in row_list:
            layer_obj = model[row][3]
            dipdir, dip, sense = self.parse_lines(
                                                layer_obj.get_data_treestore())
            for x in dipdir:
                total_dipdir.append(x)
            for y in dip:
                total_dip.append(y)

        fit_strike1, fit_dip1 = mplstereonet.fit_girdle(total_dipdir, total_dip)
        fit_strike2, fit_dip2 = mplstereonet.fit_pole(total_dipdir, total_dip)
        fit_strike3, fit_dip3 = mplstereonet.analysis._sd_of_eigenvector(
                                                   [total_dipdir, total_dip], 1)

        store = self.add_layer_dataset("line")
        self.add_linear_feature(store, fit_strike1 + 180, 90 - fit_dip1)
        self.add_linear_feature(store, fit_strike2 + 180, 90 - fit_dip2)
        self.add_linear_feature(store, fit_strike3 + 180, 90 - fit_dip3)
        self.redraw_plot()

    def on_toolbutton_new_project_clicked(self, widget):
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

    def on_toolbutton_poles_to_lines_clicked(self, widget):
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
            layer_obj = model[row][3]

            if layer_obj is None:
                return
            else:
                layer_type = layer_obj.get_layer_type()

            if layer_type == "line":
                return

        #n = new datastore
        n = self.add_layer_dataset("line")

        for row in row_list:
            layer_obj = model[row][3]
            datastore = layer_obj.get_data_treestore()
            datastore.foreach(iterate_over_data, n)

        self.redraw_plot()

    def on_toolbutton_save_clicked(self, widget):
        # pylint: disable=unused-argument
        """
        Triggered from the GUI. Saves the project.

        __!!__ Save function is not implemented yet.
        """
        pass

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
        plot_properties = StereonetProperties(self.settings, self.redraw_plot)
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

    def on_toolbutton_save_figure_clicked(self, widget):
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

    def on_toolbutton_best_plane_clicked(self, widget):
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
            layer_obj = model[row][3]
            if layer_obj.get_layer_type() == "plane":
                only_linears = False

        if only_linears is False:
            return

        total_dipdir = []
        total_dip = []
        for row in row_list:
            layer_obj = model[row][3]
            dipdir, dip, sense = self.parse_lines(
                                            layer_obj.get_data_treestore())
            for x in dipdir:
                total_dipdir.append(x)
            for y in dip:
                total_dip.append(y)

        fit_strike, fit_dip = mplstereonet.fit_girdle(total_dip, total_dipdir,
                                measurement="lines")

        store = self.add_layer_dataset("plane")
        self.add_planar_feature(store, fit_strike + 90, fit_dip)
        self.redraw_plot()

    def on_toolbutton_plane_intersect_clicked(self, widget):
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
            layer_obj = model[row][3]
            if layer_obj.get_layer_type() == "line":
                only_planes = False

        if only_planes is False:
            return

        total_dipdir = []
        total_dip = []

        #Iterate over layers and rows, gather poles
        for row in row_list:
            layer_obj = model[row][3]
            strike, dipdir, dip = self.parse_planes(
                                            layer_obj.get_data_treestore())
            for x in strike:
                total_dipdir.append(270 + x)
            for y in dip:
                total_dip.append(90 - y)
        
        self.ax_stereo.line(total_dip, total_dipdir)
        fit_strike, fit_dip = mplstereonet.fit_girdle(total_dip, total_dipdir,
                                measurement="lines")

        store = self.add_layer_dataset("line")
        self.add_linear_feature(store, fit_strike + 270, 90 - fit_dip)
        self.redraw_plot()

    def on_toolbutton_linears_to_planes_clicked(self, toolbutton):
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
            layer_obj = model[row][3]
            if layer_obj.get_layer_type() == "plane":
                only_lines = False
            elif layer_obj.get_layer_type() == "faultplane":
                only_lines = False

        if only_lines is False:
            return

        store = self.add_layer_dataset("plane")

        for row in row_list:
            layer_obj = model[row][3]
            strike, dipdir, sense = self.parse_lines(
                                            layer_obj.get_data_treestore())
            for strike, dipdir in zip(strike, dipdir):
                self.add_linear_feature(store, strike + 180, 90 - dipdir)

        self.redraw_plot()

    def layer_row_activated(self, treeview, path, column):
        """
        Double clicking a layer, opens the layer-property dialog.

        Excecutes when a treeview row is double-clicked. This passes the
        treeview-object, the path (or row) as an integer and the
        TreeViewColumn-object to this function.
        """
        layer_obj = self.layer_store[path][3]
        if layer_obj is not None:
            layer_prop = LayerProperties(layer_obj, self.redraw_plot)
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
            layer_object = model[row][3]
            child = self.sw_data.get_child()
            if layer_object is None:
                #If it has a child remove it
                if child is not None:
                    self.sw_data.remove(child)
            #Else: not a group layer
            else:
                #Get the treeview
                treeview_object = layer_object.get_data_treeview()
                #If there is a child remove it
                if child is not None:
                    self.sw_data.remove(child)
                #Add new treeview
                self.sw_data.add(treeview_object)
                self.main_window.show_all()
        else:
            child = self.sw_data.get_child()
            #If there is a child remove it
            if child is not None:
                self.sw_data.remove(child)
            #Add new treeview
            self.main_window.show_all()

    def on_layer_toggled(self, widget, path):
        # pylint: disable=unused-argument
        """
        If the layer is toggled the bool field is switched between
        True (visible) and False (invisible).
        """
        self.layer_store[path][0] = not self.layer_store[path][0]
        self.redraw_plot()

    def add_layer_dataset(self, layer_type):
        """
        Is called by the different "new layer" toolbuttons. If the number of
        selected rows are 0 or more than one, the layer is appended at the end.
        If just one row is selected, and the row is a group, then the new
        layer is created in that group. Otherwise it is added at the end of the
        same level as the selection.
        """
        store = None

        def add_layer(itr):
            if layer_type == "plane":
                store = Gtk.ListStore(float, float, str)
                view = PlaneDataView(store, self.redraw_plot)
                layer_obj = PlaneLayer(store, view)
            elif layer_type == "faultplane":
                store = Gtk.ListStore(float, float, float, float, str)
                view = FaultPlaneDataView(store, self.redraw_plot)
                layer_obj = FaultPlaneLayer(store, view)
            elif layer_type == "line":
                store = Gtk.ListStore(float, float, str)
                view = LineDataView(store, self.redraw_plot)
                layer_obj = LineLayer(store, view)
            elif layer_type == "smallcircle":
                store = Gtk.ListStore(float, float, float)
                view = SmallCircleDataView(store, self.redraw_plot)
                layer_obj = SmallCircleLayer(store, view)

            pixbuf = layer_obj.get_pixbuf()
            self.layer_store.append(itr,
                [True, pixbuf, layer_obj.get_label(), layer_obj])
            return store

        selection = self.layer_view.get_selection()
        model, row_list = selection.get_selected_rows()

        rows = len(row_list)
        if rows == 0 or rows > 1:
            store = add_layer(None)
        else:
            #If selected item is group, add to group, else: add to level
            row = row_list[0]
            layer_obj = model[row][3]
            selection_itr = model.get_iter(row_list[0])
            if layer_obj is None:
                store = add_layer(selection_itr)
            else:
                parent_itr = model.iter_parent(selection_itr)
                store = add_layer(parent_itr)

        return store

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
        Creates a new small cirlce layer.
        """
        self.add_layer_dataset("smallcircle")

    def parse_planes(self, treestore):
        """
        Parses planes and returns a list of strikes, dipdirs and dips.

        Parsing converts from dip direction to strikes.
        """
        strike = []
        dipdir = []
        dip = []
        for row in treestore:
            strike.append(float(row[0]) - 90)
            dipdir.append(float(row[0]))
            dip.append(float(row[1]))
        return strike, dipdir, dip

    def parse_faultplanes(self, treestore):
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
        for row in treestore:
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

    def parse_lines(self, treestore):
        """
        Parses linear data with the 3 columns dip direction, dip and sense.
        Returns a python-list for each column.
        """
        line_dir = []
        line_dip = []
        sense = []
        for row in treestore:
            line_dir.append(float(row[0]))
            line_dip.append(float(row[1]))
            sense.append(row[2])
        return line_dir, line_dip, sense

    def parse_smallcircles(self, treestore):
        """
        Parses small circle data. Data has 3 columns: Dip direction, dip and
        opening angle.
        """
        line_dir = []
        line_dip = []
        angle = []
        for row in treestore:
            line_dir.append(float(row[0]))
            line_dip.append(float(row[1]))
            angle.append(float(row[2]))
        return line_dir, line_dip, angle

    def draw_plane(self, layer_obj, dipdir, dip):
        """
        Function draws a great circle in the stereonet. It calls the formatting
        from the layer object.
        """
        self.ax_stereo.plane(dipdir, dip, color=layer_obj.get_line_color(),
                    label=layer_obj.get_label(),
                    linewidth=layer_obj.get_line_width(),
                    linestyle=layer_obj.get_line_style(),
                    dash_capstyle=layer_obj.get_capstyle(),
                    alpha=layer_obj.get_line_alpha(), clip_on=False)

    def draw_line(self, layer_obj, dipdir, dip):
        """
        Function draws a linear element in the stereonet. It calls the
        formatting from the layer object.
        """
        #ax.line takes dip first and then dipdir (as strike)
        self.ax_stereo.line(dip, dipdir, marker=layer_obj.get_marker_style(),
                    markersize=layer_obj.get_marker_size(),
                    color=layer_obj.get_marker_fill(),
                    label=layer_obj.get_label(),
                    markeredgewidth=layer_obj.get_marker_edge_width(),
                    markeredgecolor=layer_obj.get_marker_edge_color(),
                    alpha=layer_obj.get_marker_alpha(), clip_on=False)

    def draw_smallcircles(self, layer_obj, dipdir, dip, angle):
        """
        Function draws small circles in the stereonet. It calls the formatting
        from the layer object.
        """
        #ax.cone takes dip first and then dipdir!
        #facecolor needs to be "None" because there is a bug with which side to fill
        #Is not added to the legend yet. Matplotlib bug?
        self.ax_stereo.cone(dip, dipdir, angle, facecolor="None",
                    color=layer_obj.get_line_color(),
                    linewidth=layer_obj.get_line_width(),
                    label=layer_obj.get_label(),
                    linestyle=layer_obj.get_line_style())

    def draw_poles(self, layer_obj, dipdir, dip):
        """
        Function draws a plane pole in the stereonet. It calls the formatting
        from the layer object.
        """
        self.ax_stereo.pole(dipdir, dip, marker=layer_obj.get_pole_style(),
                    markersize=layer_obj.get_pole_size(),
                    color=layer_obj.get_pole_fill(),
                    label="Poles of {0}".format(layer_obj.get_label()),
                    markeredgewidth=layer_obj.get_pole_edge_width(),
                    markeredgecolor=layer_obj.get_pole_edge_color(),
                    alpha=layer_obj.get_pole_alpha(), clip_on=False)

    def draw_contours(self, layer_obj, dipdir, dips, measure_type):
        """
        MplStereonet accepts measurements as "poles" for planes and
        "lines" for linear measurements.
        """
        if len(dipdir) == 0:
            return None

        #Implement hatches = (['-', '+', 'x', '\\', '*', 'o', 'O', '.'])
        if layer_obj.get_draw_contour_fills() == True:
            cbar = self.ax_stereo.density_contourf(dipdir, dips,
                              measurement=measure_type,
                              method = layer_obj.get_contour_method(),
                              gridsize = layer_obj.get_contour_resolution(),
                              cmap = layer_obj.get_colormap(),
                              sigma = layer_obj.get_contour_sigma())
        else:
            cbar = None

        if layer_obj.get_draw_contour_lines() == True:
            if layer_obj.get_use_line_color() == True:
                clines = self.ax_stereo.density_contour(dipdir, dips,
                                measurement=measure_type,
                                method = layer_obj.get_contour_method(),
                                gridsize = layer_obj.get_contour_resolution(),
                                sigma = layer_obj.get_contour_sigma(),
                                colors = layer_obj.get_contour_line_color(),
                                linewidths = layer_obj.get_contour_line_width(),
                                linestyles = layer_obj.get_contour_line_style())
            else:
                clines = self.ax_stereo.density_contour(dipdir, dips,
                                measurement=measure_type,
                                method = layer_obj.get_contour_method(),
                                gridsize = layer_obj.get_contour_resolution(),
                                sigma = layer_obj.get_contour_sigma(),
                                cmap = layer_obj.get_colormap(),
                                linewidths = layer_obj.get_contour_line_width(),
                                linestyles = layer_obj.get_contour_line_style())                

        if layer_obj.get_draw_contour_labels() == True:
            if clines is not None:
                self.ax_stereo.clabel(clines,
                                fontsize = layer_obj.get_contour_label_size())

        return cbar

    def draw_hoeppener(self, layer_obj, plane_dir, plane_dip, line_dir,
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
            tree = scipy.spatial.cKDTree(plane_stack)
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

        deselected = []
        def iterate_over_rows(model, path, itr):
            layer_obj = model[path][3]
            if layer_obj is not None:
                layer_type = layer_obj.get_layer_type()
                model[path][2] = layer_obj.get_label()
                model[path][1] = layer_obj.get_pixbuf()
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

            if layer_type == "plane":
                strike, dipdir, dip = self.parse_planes(
                                            layer_obj.get_data_treestore())
                if layer_obj.get_render_gcircles() == True:
                    self.draw_plane(layer_obj, strike, dip)
                if layer_obj.get_render_poles() == True:
                    self.draw_poles(layer_obj, strike, dip)
                self.draw_contours(layer_obj, strike, dip, "poles")

                num_bins = 360 / layer_obj.get_rose_spacing()
                bin_width = 2 * np.pi / num_bins
                dipdir = np.radians(dipdir)
                values, bin_edges = np.histogram(dipdir, num_bins,
                                                     range = (0, 2 * np.pi))

                if self.ax_rose is not None:
                    self.ax_rose.bar(left = bin_edges[:-1], height = values,
                                     width = bin_width, alpha = 0.5,
                                     color = layer_obj.get_line_color(),
                                     edgecolor = layer_obj.get_pole_edge_color(),
                                     bottom = layer_obj.get_rose_bottom())

            if layer_type == "faultplane":
                strike, plane_dir, plane_dip, line_dir, line_dip, \
                    sense, line_sense_dir, line_sense_dip, \
                    lp_plane_dir, lp_plane_dip = (
                        self.parse_faultplanes(layer_obj.get_data_treestore()))

                if layer_obj.get_render_gcircles() == True:
                    self.draw_plane(layer_obj, strike, plane_dip)
                if layer_obj.get_render_poles() == True:
                    self.draw_poles(layer_obj, strike, plane_dip)
                if layer_obj.get_render_linears() == True:
                    self.draw_line(layer_obj, line_dir, line_dip)
                if layer_obj.get_draw_lp_plane() == True:
                    self.ax_stereo.plane(lp_plane_dir, lp_plane_dip,
                                         linestyle = "dotted",
                                         color = "#000000")
                if layer_obj.get_draw_hoeppener() == True:
                    self.draw_hoeppener(layer_obj, plane_dir, plane_dip,
                                        line_dir, line_dip, lp_plane_dir,
                                        lp_plane_dip, sense)

                if layer_obj.get_render_pole_contours() == True:
                    self.draw_contours(layer_obj, strike, plane_dip, "poles")
                else:
                    self.draw_contours(layer_obj, line_dip, line_dir, "lines")

            if layer_type == "line":
                dipdir, dip, sense = self.parse_lines(
                                         layer_obj.get_data_treestore())
                if layer_obj.get_render_linears() == True:
                    self.draw_line(layer_obj, dipdir, dip)
                self.draw_contours(layer_obj, dip, dipdir, "lines")

                num_bins = 360 / layer_obj.get_rose_spacing()
                bin_width = 2 * np.pi / num_bins
                dipdir = np.radians(dipdir)
                values, bin_edges = np.histogram(dipdir, num_bins,
                                                     range = (0, 2 * np.pi))

                if self.ax_rose is not None:
                    self.ax_rose.bar(left = bin_edges[:-1], height = values,
                                     width = bin_width, alpha = 0.5,
                                     color = layer_obj.get_marker_fill(),
                                     edgecolor = layer_obj.get_marker_edge_color(),
                                     bottom = layer_obj.get_rose_bottom())

            if layer_type == "smallcircle":
                dipdir, dip, angle = self.parse_smallcircles(
                                        layer_obj.get_data_treestore())
                self.draw_smallcircles(layer_obj, dipdir, dip, angle)

        self.layer_store.foreach(iterate_over_rows)

        if self.settings.get_draw_legend() == True:
            handles, labels = self.ax_stereo.get_legend_handles_labels()
            newLabels, newHandles = [], []
            for handle, label in zip(handles, labels):
                if label not in newLabels:
                    newLabels.append(label)
                    newHandles.append(handle)
            if len(handles) is not 0:
                self.ax_stereo.legend(newHandles, newLabels,
                                      bbox_to_anchor=(1.3, 1.1))
        self.canvas.draw()

            #print("Setting ticklabel")
            #labels = self.ax_stereo.get_xticklabels().tolist()
            #print(labels)
            #labels[0] = "N"
            #self.ax_stereo.set_xticklabels(labels)

    def on_toolbutton_create_group_layer_clicked(self, widget):
        """
        When the toolbutton "toolbutton_create_layer" is pressed this function
        calls the "add_layer"-function of the TreeStore. The called function
        creates a new layer-group at the end of the view.
        __!!__ Always adds to the top level.
        """
        selection = self.layer_view.get_selection()
        model, row_list = selection.get_selected_rows()
        same_depth = True

        def check_same_depth(rows):
            return rows[1:] == rows[:-1]

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
            new = model.append(parent_itr, [ov[0], ov[1], ov[2], ov[3]])
            children_left = model.iter_has_child(itr)
            while children_left == True:
                child = model.iter_children(itr)
                move_rows(new, child)
                model.remove(child)
                children_left = model.iter_has_child(itr)

        if same_depth == True and len(row_list) > 0:
            selection_itr = model.get_iter(row_list[0])
            parent_itr = model.iter_parent(selection_itr)
            new_group_itr = model.append(parent_itr,
                         [True, self.settings.get_folder_icon(),
                         "Layer group", None])
            for row in reversed(row_list):
                k = model[row]
                itr = model.get_iter(row)
                move_rows(new_group_itr, itr)
                model.remove(itr)

    def layer_name_edited(self, widget, path, new_label):
        """
        When the layer name is edited this function passes the new label to the
        TreeStore along with the correct path.
        """
        self.layer_store[path][2] = new_label
        layer_obj = self.layer_store[path][3]

        if layer_obj is not None:
            layer_obj.set_label(new_label)

        self.redraw_plot()

    def on_menuitem_about_activate(self, widget):
        """
        Triggered when the menuitem "about" is pressed. Creates an instance
        of the AboutDialog class and calls the function "run" within that class
        to show the dialog.
        """
        about = AboutDialog()
        about.run()

    def on_menuitem_quit_activate(self, widget):
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
            data_treeview = model[row][3].get_data_treeview()
            data_treestore = model[row][3].get_data_treestore()
            data_selection = data_treeview.get_selection()
            data_model, data_row_list = data_selection.get_selected_rows()
            treeiter_list = []

            for p in reversed(data_row_list):
                itr = data_model.get_iter(p)
                data_treestore.remove(itr)

            data_selection.unselect_all()

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
            
        datastore.append([dip_direct, dip, sense])

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

        datastore.append([dip_direct, dip, sense])

    def add_faultplane_feature(self, datastore, dip_direct = 0, dip = 0,
                               ldip_direct = 0, ldip = 0, sense = ""):
        """
        Adds a faultplane feature at the 
        """
        datastore.append([dip_direct, dip, ldip_direct, ldip, sense])

    def add_smallcircle_feature(self, datastore, dip_direct=0, dip=0,
                                angle=10):
        """
        Adds a small circle feature row. Defaults to an empty row unless a dip
        direction and dip are given.
        """
        datastore.append([dip_direct, dip, angle])

    def on_toolbutton_add_feature_clicked(self, widget):
        """
        Adds an empty row to the currently selected data layer.
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
                    self.add_planar_feature(data_treestore)
                if layer_type == "line":
                    self.add_linear_feature(data_treestore)
                if layer_type == "faultplane":
                    self.add_faultplane_feature(data_treestore)
                if layer_type == "smallcircle":
                    self.add_smallcircle_feature(data_treestore)

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
            current = model[layer][3]
            data_treestore = current.get_data_treestore()

            if data_treestore is not None:
                layer_type = current.get_layer_type()
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
            fc = FileChooserParse(self.run_file_parser)
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
            layer_obj = model[row][3]
            fp = FileParseDialog(text_file, layer_obj, self.redraw_plot,
                                 self.add_planar_feature,
                                 self.add_linear_feature,
                                 self.add_faultplane_feature)
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
            exportdialog = FileChooserExport(self.export_data)
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
         "poles_to_lines", "image_linears_to_planes"))

    gui_instance = MainWindow(builder)
    builder.connect_signals(gui_instance)
    Gtk.main()

if __name__ == "__main__":
    startup()
