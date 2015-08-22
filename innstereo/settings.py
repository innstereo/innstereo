#!/usr/bin/python3

"""
This module contains the AppSettings class that handles the signals of the
default-application-settings window.
"""

from gi.repository import Gtk, Gdk, Gio, GLib
from collections import OrderedDict
import os
from .i18n import i18n


class AppSettings(object):

    """
    Handles the signals of the default-application-settings window.
    """

    def __init__(self, main_window):
        """
        Initalizes the GUI. Connects to Gio.Settings. Loads the defaults.
        """
        self.builder = Gtk.Builder()
        self.builder.set_translation_domain(i18n().get_ts_domain())
        script_dir = os.path.dirname(__file__)
        rel_path = "gui_layout.glade"
        abs_path = os.path.join(script_dir, rel_path)
        self.builder.add_objects_from_file(abs_path,
            ("settings_window", "adjustment_def_pixeldens"))
        self.set_win = self.builder.get_object("settings_window")
        self.switch_def_legend = self.builder.get_object("switch_def_legend")
        self.switch_def_grid = self.builder.get_object("switch_def_grid")
        self.switch_def_cross = self.builder.get_object("switch_def_cross")
        self.radiobutton_def_area = self.builder.get_object("radiobutton_def_area")
        self.radiobutton_def_angle = self.builder.get_object("radiobutton_def_angle")
        self.switch_def_night_mode = self.builder.get_object("switch_def_night_mode")
        self.spinbutton_def_pixeldens = self.builder.get_object("spinbutton_def_pixeldens")
        self.adjustment_def_pixeldens = self.builder.get_object("adjustment_def_pixeldens")
        self.switch_def_highlight = self.builder.get_object("switch_def_highlight")
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
        pixel_density = self.g_settings.get_value("pixel-density")
        pixel_density = pixel_density.get_int32()
        self.adjustment_def_pixeldens.set_value(pixel_density)
        self.switch_def_highlight.set_active(self.g_settings.get_boolean("highlight-mode"))

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

    def on_spinbutton_def_pixeldens_value_changed(self, spinbutton):
        """
        Sets a new default for the pixel density.
        """
        value = spinbutton.get_value()
        value = GLib.Variant.new_int32(value)
        self.g_settings.set_value("pixel-density", value)

    def on_switch_def_highlight_state_set(self, switch, state):
        """
        Sets a new default for layer and feature highlighting.
        """
        self.g_settings.set_boolean("highlight-mode", state)
