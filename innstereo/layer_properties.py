#!/usr/bin/python3

"""
This module contains the layer properties dialog.

Each dialog window has its own class that controls its behaviour. This module
stores the AboutDialog-, PrintDialog-, StereonetProperties-, LayerProperties-,
and FileChooserParse-class.
"""

from gi.repository import Gtk
import matplotlib.colors as colors
import os
import numpy as np


class LayerProperties(object):

    """
    This class intializes the layer properties dialog and handles its signals.
    The init method requires a layer object, so the changes can be applied and
    a function from the main loop that redraws the plot after changes are
    applied.
    """

    def __init__(self, layer, redraw_plot, main_window):
        """
        Initializes the Gtk.Builder and loads the about dialog from glade file.
        The builder creates and instance of the about dialog and connects
        the signals.        
        """
        self.builder = Gtk.Builder()
        script_dir = os.path.dirname(__file__)
        rel_path = "gui_layout.glade"
        abs_path = os.path.join(script_dir, rel_path)
        self.builder.add_objects_from_file(abs_path,
            ("dialog_layer_properties", "liststore_line_style",
            "adjustment_line_width", "liststore_capstyle",
            "liststore_marker_style", "adjustment_marker_size",
            "adjustment_edge_width", "adjustment_pole_size",
            "adjustment_pole_edge_width", "adjustment_rose_spacing",
            "adjustment_rose_bottom", "adjustment_contour_resolution",
            "liststore_colormaps", "liststore_contour_method",
            "adjustment_contour_sigma", "adjustment_contour_label_size",
            "adjustment_lower_limit", "adjustment_upper_limit",
            "adjustment_steps"))
        self.layer = layer
        self.redraw = redraw_plot
        self.changes = []
        self.dialog = self.builder.get_object("dialog_layer_properties")
        self.dialog.set_transient_for(main_window)
        self.marker_style_dict = {".": 0, ",": 1, "o": 2, "v": 3, "^": 4, "<": 5,
                             ">": 6, "s": 7, "8": 8, "p": 9, "*": 10, "h": 11,
                             "H": 12, "+": 13, "x": 14, "D": 15, "d": 16,
                             "|": 17, "_": 18}
        self.capstyle_dict = {"butt": 0, "round": 1, "projecting": 2}
        self.line_style_dict = {"-": 0, "--": 1, "-.": 2, ":": 3}
        self.contour_method_dict = {"exponential_kamb": 0, "linear_kamb": 1,
                               "kamb": 2, "schmidt": 3}
        self.colormaps_dict = {"Blues": 0, "BuGn": 1, "BuPu": 2, "GnBu": 3,
                          "Greens": 4, "Greys": 5, "Oranges": 6, "OrRd": 7,
                          "PuBu": 8, "PuBuGn": 9, "PuRd": 10, "Purples": 11,
                          "RdPu": 12, "Reds": 13, "YlGn": 14, "YlGnBu": 15,
                          "YlOrBr": 16, "YlOrRd": 17, "afmhot": 18,
                          "autumn": 19, "bone": 20, "cool": 21, "copper": 22,
                          "gist_heat": 23, "gray": 24, "hot": 25, "pink": 26,
                          "spring": 27, "summer": 28}

        self.load_circle_properties()
        self.load_pole_properties()
        self.load_linear_properties()
        self.load_fault_properties()
        self.load_contour_properties()
        self.load_rose_properties()
        self.hide_gui_elements()
        self.set_contour_range_label()
        self.builder.connect_signals(self)

    def load_circle_properties(self):
        """
        Load default settings for great- and small circles
        """
        self.switch_render_gcircles = \
                        self.builder.get_object("switch_render_gcircles")
        self.colorbutton_line = \
                        self.builder.get_object("colorbutton_line")
        self.combobox_line_style = \
                        self.builder.get_object("combobox_line_style")
        self.spinbutton_line_width = \
                        self.builder.get_object("spinbutton_line_width")
        self.adjustment_line_width = \
                        self.builder.get_object("adjustment_line_width")
        self.combobox_capstyle = \
                        self.builder.get_object("combobox_capstyle")
        self.colorbutton_line.set_color(self.layer.get_rgba())
        self.adjustment_line_width.set_value(self.layer.get_line_width())
        self.combobox_line_style.set_active(
                              self.line_style_dict[self.layer.get_line_style()])
        self.combobox_capstyle.set_active(
                              self.capstyle_dict[self.layer.get_capstyle()])
        switch_state = self.layer.get_draw_gcircles()
        self.switch_render_gcircles.set_active(switch_state)
        self.set_gcircle_sensitivity(switch_state)

    def load_pole_properties(self):
        """
        Load default settings for pole points
        """
        self.switch_render_poles = \
                        self.builder.get_object("switch_render_poles")
        self.colorbutton_pole_fill = \
                        self.builder.get_object("colorbutton_pole_fill")
        self.colorbutton_pole_edge_color = \
                        self.builder.get_object("colorbutton_pole_edge_color")
        self.spinbutton_pole_size = \
                        self.builder.get_object("spinbutton_pole_size")
        self.adjustment_pole_size = \
                        self.builder.get_object("adjustment_pole_size")
        self.spinbutton_pole_edge_width = \
                        self.builder.get_object("spinbutton_pole_edge_width")
        self.adjustment_pole_edge_width = \
                        self.builder.get_object("adjustment_pole_edge_width")
        self.combobox_pole_style = \
                        self.builder.get_object("combobox_pole_style")
        self.colorbutton_pole_fill.set_color(self.layer.get_pole_rgba())
        self.colorbutton_pole_edge_color.set_color(
                            self.layer.get_pole_edge_rgba())
        self.adjustment_pole_size.set_value(
                            self.layer.get_pole_size())
        self.adjustment_pole_edge_width.set_value(
                            self.layer.get_pole_edge_width())
        self.combobox_pole_style.set_active(
                            self.marker_style_dict[self.layer.get_pole_style()])
        switch_state = self.layer.get_draw_poles()
        self.switch_render_poles.set_active(switch_state)
        self.set_pole_sensitivity(switch_state)

    def load_linear_properties(self):
        """
        Load the current settings for linear markers
        """
        self.switch_render_linears = \
                        self.builder.get_object("switch_render_linears")
        self.combobox_marker_style = \
                        self.builder.get_object("combobox_marker_style")
        self.spinbutton_marker_size = \
                        self.builder.get_object("spinbutton_marker_size")
        self.adjustment_marker_size = \
                        self.builder.get_object("adjustment_marker_size")
        self.colorbutton_marker = \
                        self.builder.get_object("colorbutton_marker")
        self.colorbutton_marker_edge = \
                        self.builder.get_object("colorbutton_marker_edge")
        self.spinbutton_edge_width = \
                        self.builder.get_object("spinbutton_edge_width")
        self.adjustment_marker_edge_width = \
                        self.builder.get_object("adjustment_edge_width")
        self.combobox_marker_style.set_active(
                        self.marker_style_dict[self.layer.get_marker_style()])
        self.adjustment_marker_size.set_value(self.layer.get_marker_size())
        self.colorbutton_marker.set_color(self.layer.get_marker_rgba())
        self.colorbutton_marker_edge.set_color(
                                self.layer.get_marker_edge_rgba())
        self.adjustment_marker_edge_width.set_value(
                                self.layer.get_marker_edge_width())
        switch_state = self.layer.get_draw_linears()
        self.switch_render_linears.set_active(switch_state)
        self.set_linear_sensitivity(switch_state)

    def load_fault_properties(self):
        """
        Initializes the interface for fault plots.

        Loads the ojects from the glade file using the GtkBuilder. Gets the
        current settings from the active layer and applies these settings to
        the interface.
        """
        self.checkbutton_hoeppener = \
                        self.builder.get_object("checkbutton_hoeppener")
        self.checkbutton_lp_plane = \
                        self.builder.get_object("checkbutton_lp_plane")
        self.checkbutton_hoeppener.set_active(self.layer.get_draw_hoeppener())
        self.checkbutton_lp_plane.set_active(self.layer.get_draw_lp_plane())

    def load_contour_properties(self):
        """
        Load the current settings for contours
        """
        self.switch_draw_contour_fills = \
                       self.builder.get_object("switch_draw_contour_fills")
        self.switch_contour_lines = \
                       self.builder.get_object("switch_contour_lines")
        self.combobox_contour_method = \
                        self.builder.get_object("combobox_contour_method")
        self.combobox_colormaps = \
                        self.builder.get_object("combobox_colormaps")
        self.spinbutton_contour_resolution = \
                        self.builder.get_object("spinbutton_contour_resolution")
        self.adjustment_contour_resolution = \
                        self.builder.get_object("adjustment_contour_resolution")
        self.combobox_contour_line_style = \
                        self.builder.get_object("combobox_contour_line_style")
        self.spinbutton_contour_sigma = \
                        self.builder.get_object("spinbutton_contour_sigma")
        self.adjustment_contour_sigma = \
                        self.builder.get_object("adjustment_contour_sigma")
        self.switch_contour_labels = \
                      self.builder.get_object("switch_contour_labels")
        self.spinbutton_contour_label_size = \
                        self.builder.get_object("spinbutton_contour_label_size")
        self.adjustment_contour_label_size = \
                        self.builder.get_object("adjustment_contour_label_size")
        self.switch_use_line_color = \
                        self.builder.get_object("switch_use_line_color")
        self.colorbutton_contour_line_color = \
                        self.builder.get_object("colorbutton_contour_line_color")
        self.switch_manual_range = \
                        self.builder.get_object("switch_manual_range")
        self.spinbutton_lower_limit = \
                        self.builder.get_object("spinbutton_lower_limit")
        self.spinbutton_upper_limit = \
                        self.builder.get_object("spinbutton_upper_limit")
        self.spinbutton_steps = \
                        self.builder.get_object("spinbutton_steps")
        self.adjustment_lower_limit = \
                        self.builder.get_object("adjustment_lower_limit")
        self.adjustment_upper_limit = \
                        self.builder.get_object("adjustment_upper_limit")
        self.adjustment_steps = \
                        self.builder.get_object("adjustment_steps")
        self.label_contour_steps = \
                        self.builder.get_object("label_contour_steps")
        self.switch_draw_contour_fills.set_active(
                                self.layer.get_draw_contour_fills())
        self.switch_contour_lines.set_active(
                                self.layer.get_draw_contour_lines())
        self.switch_contour_labels.set_active(
                                self.layer.get_draw_contour_labels())
        self.switch_use_line_color.set_active(self.layer.get_use_line_color())
        self.adjustment_contour_resolution.set_value(
                                            self.layer.get_contour_resolution())
        self.adjustment_contour_sigma.set_value(
                                            self.layer.get_contour_sigma())
        self.adjustment_contour_label_size.set_value(
                                            self.layer.get_contour_label_size())
        self.combobox_contour_method.set_active(
                      self.contour_method_dict[self.layer.get_contour_method()])
        self.combobox_colormaps.set_active(
                      self.colormaps_dict[self.layer.get_colormap()])
        self.combobox_contour_line_style.set_active(
                      self.line_style_dict[self.layer.get_contour_line_style()])
        self.colorbutton_contour_line_color.set_color(
                                        self.layer.get_contour_line_rgba())
        self.adjustment_lower_limit.set_value(self.layer.get_lower_limit())
        self.adjustment_upper_limit.set_value(self.layer.get_upper_limit())
        self.adjustment_steps.set_value(self.layer.get_steps())
        self.switch_draw_contour_fills.set_active(self.layer.get_draw_contour_fills())
        self.set_contour_sensitivity()
        manual_range_state = self.layer.get_manual_range()
        self.switch_manual_range.set_active(manual_range_state)
        self.set_manual_range_sensitivity(manual_range_state)        

    def load_rose_properties(self):
        """
        Load the current settings for the rose diagram
        """
        self.spinbutton_rose_spacing = \
                        self.builder.get_object("spinbutton_rose_spacing")
        self.adjustment_rose_spacing = \
                        self.builder.get_object("adjustment_rose_spacing")
        self.spinbutton_rose_bottom = \
                        self.builder.get_object("spinbutton_rose_bottom")
        self.adjustment_rose_bottom = \
                        self.builder.get_object("adjustment_rose_bottom")
        self.adjustment_rose_spacing.set_value(self.layer.get_rose_spacing())
        self.adjustment_rose_bottom.set_value(self.layer.get_rose_bottom())

    def hide_gui_elements(self):
        """
        Hides some elements of the GUI depending on the layer type

        Pages:
        0: Great and Small Circles
        1: Poles
        2: Lines
        3: Fault Plots
        4: Contours
        5: Rose Diagram
        """
        self.notebook = \
                        self.builder.get_object("notebook1")
        layertype = self.layer.get_layer_type()
        if layertype == "line":
            self.notebook.get_nth_page(0).hide()
            self.notebook.get_nth_page(1).hide()
            self.notebook.get_nth_page(3).hide()
        elif layertype == "plane":
            self.notebook.get_nth_page(2).hide()
            self.notebook.get_nth_page(3).hide()
        elif layertype == "smallcircle":
            self.notebook.get_nth_page(1).hide()
            self.notebook.get_nth_page(2).hide()
            self.notebook.get_nth_page(3).hide()
            self.notebook.get_nth_page(4).hide()
            self.notebook.get_nth_page(5).hide()
        elif layertype == "faultplane":
            self.notebook.get_nth_page(4).hide()
        elif layertype == "eigenvector":
            self.notebook.get_nth_page(0).hide()
            self.notebook.get_nth_page(1).hide()
            self.notebook.get_nth_page(3).hide()
            self.notebook.get_nth_page(4).hide()
        self.notebook.set_current_page(self.layer.get_page())

    def on_switch_render_linears_state_set(self, switch, state):
        """
        Queues up the new state for rendering linears.

        When the state of the render linears switch is changed this method is
        called and queues up the new state in the the list of changes.
        """
        self.changes.append(lambda: self.layer.set_draw_linears(state))
        self.set_linear_sensitivity(state)

    def on_entry_layer_name_changed(self, entry):
        """
        Triggered when the layer name is changed. Reads out the text buffer and
        stores the name as a string in a temporary variable.
        """
        buffer_obj = entry.get_buffer()
        new_label = buffer_obj.get_text()
        self.changes.append(lambda: self.layer.set_label(new_label))

    def on_switch_render_gcircles_state_set(self, checkbutton, state):
        """
        Queues up the new state for great and small circles.

        When the state of the great and samll circle switch is changed this
        method is called and queues up the new state in the the list of changes.
        """
        self.changes.append(lambda: self.layer.set_draw_gcircles(state))
        self.set_gcircle_sensitivity(state)

    def set_gcircle_sensitivity(self, state):
        """
        Sets widgets sensitivity according to the great circle switch.

        When the switch is turned off, the widgets for line properties are
        not nedded and the sensitivity turned off.
        """
        self.colorbutton_line.set_sensitive(state)
        self.combobox_line_style.set_sensitive(state)
        self.combobox_capstyle.set_sensitive(state)
        self.spinbutton_line_width.set_sensitive(state)

    def set_linear_sensitivity(self, state):
        """
        Sets widgets sensitivity according to the linear feature switch.

        When the switch is turned off, the widgets for linears customization are
        not nedded and the sensitivity turned off.
        """
        self.combobox_marker_style.set_sensitive(state)
        self.spinbutton_marker_size.set_sensitive(state)
        self.colorbutton_marker.set_sensitive(state)
        self.colorbutton_marker_edge.set_sensitive(state)
        self.spinbutton_edge_width.set_sensitive(state)

    def set_pole_sensitivity(self, state):
        """
        Sets widgets sensitivity according to the pole-marker switch.

        When the switch is turned off, the widgets for pole customization are
        not nedded and the sensitivity turned off.
        """
        self.colorbutton_pole_fill.set_sensitive(state)
        self.colorbutton_pole_edge_color.set_sensitive(state)
        self.spinbutton_pole_size.set_sensitive(state)
        self.spinbutton_pole_edge_width.set_sensitive(state)
        self.combobox_pole_style.set_sensitive(state)

    def set_manual_range_sensitivity(self, state):
        """
        Sets widgets sensitivity according to the manual range switch.

        When the switch is turned off, the widgets for the range customization
        are not nedded and the sensitivity turned off.
        """
        self.spinbutton_lower_limit.set_sensitive(state)
        self.spinbutton_upper_limit.set_sensitive(state)
        self.spinbutton_steps.set_sensitive(state)

    def set_contour_sensitivity(self):
        """
        Turns sensitivity of widget in the contour page on or off.

        Depending on which switches are on or off, widget that don't change
        the plot are set unsensitive.
        """
        fill = self.switch_draw_contour_fills.get_active()
        line = self.switch_contour_lines.get_active()
        label = self.switch_contour_labels.get_active()
        line_color = self.switch_use_line_color.get_active()
        if line == True:
            self.switch_contour_labels.set_sensitive(True)
            if label == True:
                self.spinbutton_contour_label_size.set_sensitive(True)
            else:
                self.spinbutton_contour_label_size.set_sensitive(False)
            self.combobox_contour_line_style.set_sensitive(True)
            self.switch_use_line_color.set_sensitive(True)
            if line_color == True:
                self.colorbutton_contour_line_color.set_sensitive(True)
            else:
                self.colorbutton_contour_line_color.set_sensitive(False)
        else:
            self.switch_contour_labels.set_sensitive(False)
            self.spinbutton_contour_label_size.set_sensitive(False)
            self.combobox_contour_line_style.set_sensitive(False)
            self.switch_use_line_color.set_sensitive(False)
            self.colorbutton_contour_line_color.set_sensitive(False)

        if line == True or fill == True:
            self.combobox_colormaps.set_sensitive(True)
        else:
            self.combobox_colormaps.set_sensitive(False)

    def on_switch_render_poles_state_set(self, switch, state):
        """
        Queues up the new state for rendering poles.

        When the state of the render poles switch is changed this method is
        called and queues up the new state in the the list of changes.
        """
        self.changes.append(lambda: self.layer.set_draw_poles(state))
        self.set_pole_sensitivity(state)

    def on_colorbutton_choose_line_color_color_set(self, color_button):
        """
        Triggered when the line color is changed. The function receives
        a Gtk.ColorButton instance. Queues up the new line color in the
        list of changes.
        """
        rgba = color_button.get_rgba()
        rgb_str = rgba.to_string()
        red, green, blue = rgb_str[4:-1].split(",")
        color_list = [int(red)/255, int(green)/255, int(blue)/255]
        new_line_color_hex = colors.rgb2hex(color_list)
        self.changes.append(lambda: self.layer.set_line_color(
                                                new_line_color_hex))

    def on_combobox_line_style_changed(self, combo):
        """
        Queues up the new line style in the list of changes.
        """
        combo_iter = combo.get_active_iter()
        if combo_iter != None:
            model = combo.get_model()
            new_line_style = model[combo_iter][1]
            self.changes.append(lambda: self.layer.set_line_style(
                                new_line_style))

    def on_spinbutton_line_width_value_changed(self, spinbutton):
        """
        Queues up the new line width in the list of changes.
        """
        new_line_width = spinbutton.get_value()
        self.changes.append(lambda: self.layer.set_line_width(new_line_width))

    def on_combobox_capstyle_changed(self, combo):
        """
        Queues up the new capstyle in the list of changes.
        """
        combo_iter = combo.get_active_iter()
        if combo_iter != None:
            model = combo.get_model()
            new_capstyle = model[combo_iter][1]
            self.changes.append(lambda: self.layer.set_capstyle(new_capstyle))

    def on_colorbutton_pole_fill_color_set(self, colorbutton):
        """
        Queues up the new pole fill color in the list of changes.
        """
        rgba = colorbutton.get_rgba()
        rgb_str = rgba.to_string()
        red, green, blue = rgb_str[4:-1].split(",")
        color_list = [int(red)/255, int(green)/255, int(blue)/255]
        new_pole_color_hex = colors.rgb2hex(color_list)
        self.changes.append(lambda: self.layer.set_pole_fill(
                                                new_pole_color_hex))

    def on_colorbutton_pole_edge_color_color_set(self, colorbutton):
        """
        Queues up the new pole edge color in the list of changes.
        """
        rgba = colorbutton.get_rgba()
        rgb_str = rgba.to_string()
        red, green, blue = rgb_str[4:-1].split(",")
        color_list = [int(red)/255, int(green)/255, int(blue)/255]
        new_pole_edge_color_hex = colors.rgb2hex(color_list)
        self.changes.append(lambda: self.layer.set_pole_edge_color(
                                                new_pole_edge_color_hex))

    def on_combobox_pole_style_changed(self, combobox):
        """
        Queues up the new pole style in the list of changes.
        """
        combo_iter = combobox.get_active_iter()
        if combo_iter != None:
            model = combobox.get_model()
            new_pole_style = model[combo_iter][1]
            self.changes.append(lambda: self.layer.set_pole_style(
                                                    new_pole_style))

    def on_spinbutton_pole_size_value_changed(self, spinbutton):
        """
        Queues up the new pole size in the list of changes.
        """
        new_pole_size = spinbutton.get_value()
        self.changes.append(lambda: self.layer.set_pole_size(new_pole_size))

    def on_spinbutton_pole_edge_width_value_changed(self, spinbutton):
        """
        Queues up the new pole edge width in the list of changes.
        """
        new_pole_edge_width = spinbutton.get_value()
        self.changes.append(lambda: self.layer.set_pole_edge_width(
                            new_pole_edge_width))

    def on_colorbutton_marker_color_set(self, color_button):
        """
        Queues up the new marker fill color in the list of changes.
        """
        rgba = color_button.get_rgba()
        rgb_str = rgba.to_string()
        red, green, blue = rgb_str[4:-1].split(",")
        color_list = [int(red)/255, int(green)/255, int(blue)/255]
        new_marker_color_hex = colors.rgb2hex(color_list)
        self.changes.append(lambda: self.layer.set_marker_fill(
                                                new_marker_color_hex))

    def on_colorbutton_marker_edge_color_set(self, color_button):
        """
        Queues up the new marker edge color in the list of changes.
        """
        rgba = color_button.get_rgba()
        rgb_str = rgba.to_string()
        red, green, blue = rgb_str[4:-1].split(",")
        color_list = [int(red)/255, int(green)/255, int(blue)/255]
        new_marker_edge_color_hex = colors.rgb2hex(color_list)
        self.changes.append(lambda: self.layer.set_marker_edge_color(
                                                new_marker_edge_color_hex))
        
    def on_combobox_marker_style_changed(self, combo):
        """
        Queues up the new marker style width in the list of changes.
        """
        combo_iter = combo.get_active_iter()
        if combo_iter != None:
            model = combo.get_model()
            new_marker_style = model[combo_iter][1]
            self.changes.append(lambda: self.layer.set_marker_style(
                                                    new_marker_style))

    def on_spinbutton_marker_size_value_changed(self, spinbutton):
        """
        Queues up the new marker size in the list of changes.
        """
        new_marker_size = spinbutton.get_value()
        self.changes.append(lambda: self.layer.set_marker_size(new_marker_size))

    def on_spinbutton_edge_width_value_changed(self, spinbutton):
        """
        Queues up the new marker edge width in the list of changes.
        """
        new_marker_edge_width = spinbutton.get_value()
        self.changes.append(lambda: self.layer.set_marker_edge_width(
                                                    new_marker_edge_width))

    def on_dialog_layer_properties_close(self, widget):
        """
        Hides the dialog when the dialog is closed.
        """
        self.dialog.hide()

    def on_dialog_layer_properties_response(self, widget, signal):
        """
        Hides the dialog if a response is triggered.
        """
        self.dialog.hide()

    def on_button_layerproperties_cancel_clicked(self, widget):
        """
        If the dialog is canceled the changes are discarded (automatically),
        and the window is hidden.
        """
        self.layer.set_page(self.notebook.get_current_page())
        self.dialog.hide()

    def on_button_layerproperties_apply_clicked(self, widget):
        """
        When apply is pressed this function applies all changes and closes
        the dialog window.
        """
        for change in self.changes:
            change()
        
        self.layer.set_page(self.notebook.get_current_page())
        self.redraw()
        self.dialog.hide()

    def run(self):
        """
        This function is run when the about dialog is called from the main
        window. It shows the about dialog.
        """
        self.dialog.run()

    def on_dialog_layer_properties_destroy(self, widget):
        """
        This function is run when the about dialog is closed with the x-button
        in the title bar. It hides the about dialog.
        """
        self.dialog.hide()

    def on_spinbutton_rose_spacing_value_changed(self, spinbutton):
        """
        Triggered when the value in the spinbutton for the spacing of the
        rose diagram is changed. Queues up the new value in the list of changes.
        """
        new_rose_spacing = spinbutton.get_value()
        self.changes.append(lambda: self.layer.set_rose_spacing(
                                                    new_rose_spacing))

    def on_spinbutton_rose_bottom_value_changed(self, spinbutton):
        """
        Triggered when the value in the spinbutton for the bottom cutoff of the
        rose diagram is changed. Queues up the new value in the list of changes.
        """
        new_rose_bottom = spinbutton.get_value()
        self.changes.append(lambda: self.layer.set_rose_bottom(
                                                    new_rose_bottom))

    def on_switch_draw_contour_fills_state_set(self, switch, state):
        """
        Triggered when the state of the checkbutton for rendering contour fills
        is toggled. Queues up the new state in the list of changes.
        """
        self.changes.append(lambda: self.layer.set_draw_contour_fills(state))
        self.set_contour_sensitivity()

    def on_switch_contour_lines_state_set(self, checkbutton, state):
        """
        Triggered when the state of the checkbutton for rendering contour lines
        is toggled. Queues up the new state in the list of changes.
        """
        self.changes.append(lambda: self.layer.set_draw_contour_lines(state))
        self.set_contour_sensitivity()

    def on_combobox_contour_method_changed(self, combobox):
        """
        Triggered when a new contouring method is chosen. Queues up the
        new colormap in the list of changes.
        """
        combo_iter = combobox.get_active_iter()
        if combo_iter != None:
            model = combobox.get_model()
            new_method = model[combo_iter][1]
            self.changes.append(
                    lambda: self.layer.set_contour_method(new_method))

    def on_spinbutton_contour_resolution_value_changed(self, spinbutton):
        """
        Triggered when the grid reolution for the contours is changed. Converts
        value to int just to be safe. Queues up the int value in the list of
        changes. Values below 3 don't work and above 300 are too slow for
        rendering. These limits are set in Glade in the 
        "adjustment_contour_resolution".
        """
        new_contour_resolution = int(spinbutton.get_value())
        self.changes.append(
             lambda: self.layer.set_contour_resolution(new_contour_resolution))

    def on_combobox_colormaps_changed(self, combobox):
        """
        Triggered when the colormap is changed. The new colormap is queued up
        in the list of changes. Colormap is a string (e.g. "hot")
        """
        combo_iter = combobox.get_active_iter()
        if combo_iter != None:
            model = combobox.get_model()
            new_colormap = model[combo_iter][0]
            self.changes.append(
                lambda: self.layer.set_colormap(new_colormap))

    def on_combobox_contour_line_style_changed(self, combobox):
        """
        Triggered when the contour-lines line-style is changed. Queues up the
        new style in the list of changes.
        """
        combo_iter = combobox.get_active_iter()
        if combo_iter != None:
            model = combobox.get_model()
            new_line_style = model[combo_iter][1]
            self.changes.append(
                lambda: self.layer.set_contour_line_style(new_line_style))

    def on_spinbutton_contour_sigma_value_changed(self, spinbutton):
        """
        Triggered when the standard deviation for contouring is changed.
        Queues up the new value in the list of changes.
        """
        new_contour_sigma = int(spinbutton.get_value())
        self.changes.append(
             lambda: self.layer.set_contour_sigma(new_contour_sigma))

    def on_switch_contour_labels_state_set(self, switch, state):
        """
        Triggerd when the checkbutton to draw contour labels is toggeled.
        Queues up the new state in the list of changes.
        """
        self.changes.append(lambda: self.layer.set_draw_contour_labels(state))
        self.set_contour_sensitivity()

    def on_spinbutton_contour_label_size_value_changed(self, spinbutton):
        """
        Triggered when the font size for contour labels is changed. The new
        value is queued up in the list of changes.
        """
        label_size = int(spinbutton.get_value())
        self.changes.append(
             lambda: self.layer.set_contour_label_size(label_size))

    def on_switch_use_line_color_state_set(self, switch, state):
        """
        Queues up the new state for using line colors for contour lines.

        When the state of the line color switch is changed this method is
        called and queues up the new state in the the list of changes.
        """
        self.changes.append(lambda: self.layer.set_use_line_color(state))
        self.set_contour_sensitivity()

    def on_colorbutton_contour_line_color_color_set(self, colorbutton):
        """
        Queues up the new contour line color in the list of changes.
        """
        rgba = colorbutton.get_rgba()
        rgb_str = rgba.to_string()
        red, green, blue = rgb_str[4:-1].split(",")
        color_list = [int(red)/255, int(green)/255, int(blue)/255]
        new_color = colors.rgb2hex(color_list)
        self.changes.append(
                    lambda: self.layer.set_contour_line_color(new_color))

    def on_checkbutton_lp_plane_toggled(self, checkbutton):
        """
        Queues up a new state for the linear-pole-plane checkbutton.

        Triggered when a new state for the linear-pole-plane checkbutton
        is set. Gets the new state and queues it up in the list of changes.
        """
        draw_lp_plane = checkbutton.get_active()
        self.changes.append(
            lambda: self.layer.set_draw_lp_plane(draw_lp_plane))

    def on_checkbutton_hoeppener_toggled(self, checkbutton):
        """
        Queues up a new state for the draw Hoeppener checkbutton.

        Triggered when a new state for the Hoeppener checkbutton
        is set. Gets the new state and queues it up in the list of changes.
        """
        draw_hoeppener = checkbutton.get_active()
        self.changes.append(
            lambda: self.layer.set_draw_hoeppener(draw_hoeppener))

    def on_switch_manual_range_state_set(self, switch, state):
        """
        Queues up the new state of the manual range for contours switch.

        The new state, a boolean, is queued up in the list of changes, and is
        only applied if the "Apply" button is pressed.
        """
        self.changes.append(lambda: self.layer.set_manual_range(state))
        self.set_contour_range_label()
        self.set_manual_range_sensitivity(state)

    def set_contour_range_label(self):
        """
        Turns the display of the resulting contour interval on or off.

        When the manual range switch is on, then the resulting contour steps
        are displayed in the dialog. When switch is off, the label is empty.
        """
        if self.switch_manual_range.get_active() == True:
            lower = self.spinbutton_lower_limit.get_value()
            upper = self.spinbutton_upper_limit.get_value()
            steps = self.spinbutton_steps.get_value()
            spacing = np.linspace(lower, upper, num=steps).round(2)
            self.label_contour_steps.set_text(str(spacing))
        else:
            self.label_contour_steps.set_text("")

    def on_spinbutton_lower_limit_value_changed(self, spinbutton):
        """
        Queues up the new lower limit for contours in the list of changes.

        When the lower limit is changed, this method is called and queues up
        the new value in the list of changes.
        """
        lower_limit = spinbutton.get_value()
        self.changes.append(lambda: self.layer.set_lower_limit(lower_limit))
        self.set_contour_range_label()

    def on_spinbutton_upper_limit_value_changed(self, spinbutton):
        """
        Queues up the new upper limit for contours in the list of changes.

        When the upper limit is changed, this method is called and queues up
        the new value in the list of changes.
        """
        upper_limit = spinbutton.get_value()
        self.changes.append(lambda: self.layer.set_upper_limit(upper_limit))
        self.set_contour_range_label()

    def on_spinbutton_steps_value_changed(self, spinbutton):
        """
        Queues up the new number of steps for contours in the list of changes.

        When the number of steps is changed, this method is called and queues up
        the new value in the list of changes.
        """
        steps = spinbutton.get_value()
        self.changes.append(lambda: self.layer.set_steps(steps))
        self.set_contour_range_label()

