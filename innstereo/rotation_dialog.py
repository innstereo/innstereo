#!/usr/bin/python3

"""
This module stores the RotationDialog class which controls the rotation dialog.

The module contains only the RotationDialog class. It controls the behaviour
of the data-rotation dialog.
"""

from gi.repository import Gtk
from matplotlib.figure import Figure
from matplotlib.gridspec import GridSpec
from matplotlib.backends.backend_gtk3cairo import (FigureCanvasGTK3Cairo
                                                   as FigureCanvas)
import numpy as np
import mplstereonet
import os


class RotationDialog(object):

    """
    This class controls the appearance and signals of the data-rotation dialog.

    This class pulls the rotation dialog from the Glade file, intilizes the
    widgets and has methods for the signals defined in Glade.
    """

    def __init__(self, main_window, settings, data, add_layer_dataset, add_feature, redraw_main):
        """
        Initializes the RotationDialog class.

        Requires the main_window object, the settings object (PlotSettings
        class) and the data rows to initialize. All the necessary widgets are
        loaded from the Glade file. A matplotlib figure is set up and added
        to the scrolledwindow. Two axes are set up that show the original and
        rotated data.
        """
        self.builder = Gtk.Builder()
        script_dir = os.path.dirname(__file__)
        rel_path = "gui_layout.glade"
        abs_path = os.path.join(script_dir, rel_path)
        self.builder.add_objects_from_file(abs_path,
            ("dialog_rotation", "adjustment_rotation_dipdir",
             "adjustment_rotation_dip", "adjustment_rotation_angle"))
        self.dialog = self.builder.get_object("dialog_rotation")
        self.dialog.set_transient_for(main_window)
        self.settings = settings
        self.data = data
        self.trans = self.settings.get_transform()
        self.add_layer_dataset = add_layer_dataset
        self.add_feature = add_feature
        self.redraw_main = redraw_main

        self.adjustment_rotation_dipdir = self.builder.get_object("adjustment_rotation_dipdir")
        self.adjustment_rotation_dip = self.builder.get_object("adjustment_rotation_dip")
        self.adjustment_rotation_angle = self.builder.get_object("adjustment_rotation_angle")

        self.spinbutton_rotation_dipdir = self.builder.get_object("spinbutton_rotation_dipdir")
        self.spinbutton_rotation_dip = self.builder.get_object("spinbutton_rotation_dip")
        self.spinbutton_rotation_angle = self.builder.get_object("spinbutton_rotation_angle")

        self.scrolledwindow_rotate = self.builder.get_object("scrolledwindow_rotate")

        self.fig = Figure(dpi=self.settings.pixel_density)
        self.canvas = FigureCanvas(self.fig)
        self.scrolledwindow_rotate.add_with_viewport(self.canvas)

        gridspec = GridSpec(1, 2)
        original_sp = gridspec.new_subplotspec((0, 0),
                                             rowspan=1, colspan=1)
        rotated_sp = gridspec.new_subplotspec((0, 1),
                                           rowspan=1, colspan=1)
        self.original_ax = self.fig.add_subplot(original_sp,
                                         projection=self.settings.get_projection())
        self.rotated_ax = self.fig.add_subplot(rotated_sp,
                                         projection=self.settings.get_projection())

        self.canvas.draw()
        self.redraw_plot()
        self.dialog.show_all()
        self.builder.connect_signals(self)

    def run(self):
        """
        Runs the dialog.

        Called from the MainWindow class. Initializes and shows the dialog.
        """
        self.dialog.run()

    def on_dialog_rotation_destroy(self, widget):
        """
        Hides the dialog on destroy.

        When the dialog is destroyed it is hidden.
        """
        self.dialog.hide()

    def on_button_cancel_rotation_clicked(self, button):
        """
        Exits the rotation dialog and makes no changes to the project.

        When the user clicks on Cancel the dialog is hidden, and no changes
        are made to the project structure.
        """
        self.dialog.hide()

    def on_button_apply_rotate_clicked(self, button):
        """
        Adds the rotated layers to the project.

        When the user clicks on "apply the rotation", the rotated data is
        added to the project as new datasets.
        """
        raxis_dipdir = self.spinbutton_rotation_dipdir.get_value()
        raxis_dip = self.spinbutton_rotation_dip.get_value()
        raxis = [raxis_dipdir, raxis_dip]
        raxis_angle = self.spinbutton_rotation_angle.get_value()

        for lyr_obj in self.data:
            key = 0
            dipdir_lst = []
            dips_lst = []
            sense = []
            layer_type = lyr_obj.get_layer_type()
            layer_data = lyr_obj.get_data_treestore()
            for row in layer_data:
                dipdir, dip = self.rotate_data(raxis, raxis_angle, row[0], row[1])
                if layer_type == "plane":
                    dipdir_lst.append(dipdir)
                else:
                    dipdir_lst.append(dipdir)
                dips_lst.append(dip)
                sense.append(row[2])

            if layer_type == "line":
                store = self.add_layer_dataset("line")
                for dipdir, dip in zip(dipdir_lst, dips_lst):
                    self.add_feature("line", store, dipdir, dip, sense[key])
                    key += 1
                
            if layer_type == "plane":
                store = self.add_layer_dataset("plane")
                for dipdir, dip in zip(dipdir_lst, dips_lst):
                    self.add_feature("plane", store, dipdir, dip, sense[key])
                    key += 1

        self.dialog.hide()
        self.redraw_main()

    def on_spinbutton_rotation_dipdir_value_changed(self, spinbutton):
        """
        Redraws the plot.

        When the value of the spinbutton is changed, the redraw_plot method
        is called, which rotates the data according to the new setting.
        """
        self.redraw_plot()

    def on_spinbutton_rotation_dip_value_changed(self, spinbutton):
        """
        Redraws the plot.

        When the value of the spinbutton is changed, the redraw_plot method
        is called, which rotates the data according to the new setting.
        """
        self.redraw_plot()

    def on_spinbutton_rotation_angle_value_changed(self, spinbutton):
        """
        Redraws the plot.

        When the value of the spinbutton is changed, the redraw_plot method
        is called, which rotates the data according to the new setting.
        """
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

    def redraw_plot(self):
        """
        Redraws the plot using the current settings of the dialog's spinbuttons.

        This method clears the two axes and adds the annotations. The current
        values of the rotation axis and rotation angle spinbuttons are
        retrieved. The data is parsed, and the features are then drawn.
        In addition the rotation-axis is drawn.
        """
        self.original_ax.cla()
        self.rotated_ax.cla()
        self.original_ax.grid(False)
        self.rotated_ax.grid(False)
        self.original_ax.set_azimuth_ticks([0], labels=["N"])
        self.rotated_ax.set_azimuth_ticks([0], labels=["N"])

        bar = 0.05
        self.original_ax.annotate("", xy = (-bar, 0),
                                    xytext = (bar, 0),
                                    xycoords = "data",
                                    arrowprops = dict(arrowstyle = "-",
                                                      connectionstyle = "arc3"))
        self.original_ax.annotate("", xy = (0, -bar),
                                    xytext = (0, bar),
                                    xycoords = "data",
                                    arrowprops = dict(arrowstyle = "-",
                                                      connectionstyle = "arc3"))
        self.rotated_ax.annotate("", xy = (-bar, 0),
                                    xytext = (bar, 0),
                                    xycoords = "data",
                                    arrowprops = dict(arrowstyle = "-",
                                                      connectionstyle = "arc3"))
        self.rotated_ax.annotate("", xy = (0, -bar),
                                    xytext = (0, bar),
                                    xycoords = "data",
                                    arrowprops = dict(arrowstyle = "-",
                                                      connectionstyle = "arc3"))

        raxis_dipdir = self.spinbutton_rotation_dipdir.get_value()
        raxis_dip = self.spinbutton_rotation_dip.get_value()
        raxis = [raxis_dipdir, raxis_dip]
        raxis_angle = self.spinbutton_rotation_angle.get_value()

        for lyr_obj in self.data:
            dipdir_org = []
            dips_org = []
            dipdir_lst = []
            dips_lst = []
            layer_type = lyr_obj.get_layer_type()
            layer_data = lyr_obj.get_data_treestore()
            for row in layer_data:
                if layer_type == "plane":
                    dipdir_org.append(row[0] - 90)
                else:
                    dipdir_org.append(row[0])
                dips_org.append(row[1])
                dipdir, dip = self.rotate_data(raxis, raxis_angle, row[0], row[1])
                if layer_type == "plane":
                    dipdir_lst.append(dipdir - 90)
                else:
                    dipdir_lst.append(dipdir)
                dips_lst.append(dip)

            if layer_type == "line":
                self.original_ax.line(dips_org, dipdir_org,
                    marker=lyr_obj.get_marker_style(),
                    markersize=lyr_obj.get_marker_size(),
                    color=lyr_obj.get_marker_fill(),
                    markeredgewidth=lyr_obj.get_marker_edge_width(),
                    markeredgecolor=lyr_obj.get_marker_edge_color(),
                    alpha=lyr_obj.get_marker_alpha(), clip_on=False)
                self.rotated_ax.line(dips_lst, dipdir_lst,
                    marker=lyr_obj.get_marker_style(),
                    markersize=lyr_obj.get_marker_size(),
                    color=lyr_obj.get_marker_fill(),
                    markeredgewidth=lyr_obj.get_marker_edge_width(),
                    markeredgecolor=lyr_obj.get_marker_edge_color(),
                    alpha=lyr_obj.get_marker_alpha(), clip_on=False)

            if layer_type == "plane":
                self.original_ax.plane(dipdir_org, dips_org, color=lyr_obj.get_line_color(),
                    linewidth=lyr_obj.get_line_width(),
                    linestyle=lyr_obj.get_line_style(),
                    dash_capstyle=lyr_obj.get_capstyle(),
                    alpha=lyr_obj.get_line_alpha(), clip_on=False)
                self.rotated_ax.plane(dipdir_lst, dips_lst, color=lyr_obj.get_line_color(),
                    linewidth=lyr_obj.get_line_width(),
                    linestyle=lyr_obj.get_line_style(),
                    dash_capstyle=lyr_obj.get_capstyle(),
                    alpha=lyr_obj.get_line_alpha(), clip_on=False)

        #Plot rotation axis
        self.original_ax.line(raxis_dip, raxis_dipdir, marker="o",
                    markersize=10, color="#ff0000",
                    markeredgewidth=1, markeredgecolor="#000000",
                    alpha=1, clip_on=False)

        self.canvas.draw()
