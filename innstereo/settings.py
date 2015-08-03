#!/usr/bin/python3

"""
This module contains the AppSettings class that handles the signals of the
default-application-settings window.
"""

from gi.repository import Gtk, Gdk, Gio
from collections import OrderedDict
import os


class AppSettings(object):

    """
    Handles the signals of the default-application-settings window.
    """

    def __init__(self, main_window):
        """
        Initalizes the GUI. Connects to Gio.Settings. Loads the defaults.
        """
        self.builder = Gtk.Builder()
        script_dir = os.path.dirname(__file__)
        rel_path = "gui_layout.glade"
        abs_path = os.path.join(script_dir, rel_path)
        self.builder.add_objects_from_file(abs_path,
            ("settings_window", ""))
        self.set_win = self.builder.get_object("settings_window")
        self.switch_def_legend = self.builder.get_object("switch_def_legend")
        self.switch_def_grid = self.builder.get_object("switch_def_grid")
        self.switch_def_cross = self.builder.get_object("switch_def_cross")
        self.radiobutton_def_area = self.builder.get_object("radiobutton_def_area")
        self.radiobutton_def_angle = self.builder.get_object("radiobutton_def_angle")
        self.switch_def_night_mode = self.builder.get_object("switch_def_night_mode")
        self.set_win.set_transient_for(main_window)
        self.builder.connect_signals(self)

        self.g_settings = Gio.Settings.new("org.gtk.innstereo")
        self.get_defaults()

    def get_defaults(self):
        """
        Loads the defaults from the Gio.Settings and applies them to the GUI.
        """
        self.switch_def_legend.set_active(self.g_settings.get_boolean("show-legend"))
        self.switch_def_grid.set_active(self.g_settings.get_boolean("draw-grid"))
        self.switch_def_cross.set_active(self.g_settings.get_boolean("center-cross"))
        projection = self.g_settings.get_boolean("stereonet-projection")
        if projection == True:
            self.radiobutton_def_area.set_active(True)
        else:
            self.radiobutton_def_angle.set_active(True)
        self.switch_def_night_mode.set_active(self.g_settings.get_boolean("night-mode"))

    def on_settings_window_destroy(self, widget):
        """
        Hides the window.
        """
        self.set_win.hide()

    def run(self):
        """
        Shows the window.
        """
        self.set_win.show()

    def on_switch_def_legend_state_set(self, switch, state):
        """
        Sets a new state for whether the legend should be drawn by default.
        """
        self.g_settings.set_boolean("show-legend", state)

    def on_switch_def_grid_state_set(self, switch, state):
        """
        Sets a new state for whether the grid should be drawn by default.
        """
        self.g_settings.set_boolean("draw-grid", state)

    def on_switch_def_cross_state_set(self, switch, state):
        """
        Sets a new state for whether the cross should be drawn by default.
        """
        self.g_settings.set_boolean("center-cross", state)

    def on_radiobutton_def_area_toggled(self, radiobutton):
        """
        Sets a new state for which projection should be used by default.
        """
        state = radiobutton.get_active()
        self.g_settings.set_boolean("stereonet-projection", state)

    def on_switch_def_night_mode_state_set(self, switch, state):
        """
        Sets a new state for whether the interface should default to dark.
        """
        self.g_settings.set_boolean("night-mode", state)                
