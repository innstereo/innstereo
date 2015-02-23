#!/usr/bin/python3

"""
This module contains dialog windows.

Each dialog window has its own class that controls its behaviour. This module
stores the AboutDialog-, PrintDialog-, StereonetProperties-, LayerProperties-,
and FileChooserParse-class.
"""

from gi.repository import Gtk
import matplotlib.colors as colors


class AboutDialog(object):

    """
    This class controls the about dialog and handles its signals.

    The layout and content of the About Dialog is stored in the Glade file.
    This class parses the glade file for the dialog, and connects the signals
    that are declared in Glade.
    """

    def __init__(self):
        """
        Initializes the About dialog.

        Loads the Gtk.Builder and parses the Glade file. Then the signals, that
        are declared in the Glade file are connected to this class.
        """
        self.builder = Gtk.Builder()
        self.builder.add_objects_from_file("gui_layout.glade",
            ("aboutdialog", ""))
        self.ab = self.builder.get_object("aboutdialog")
        self.builder.connect_signals(self)

    def run(self):
        """
        This function is run when the about dialog is called from the main
        window. It shows the about dialog.
        """
        self.ab.run()

    def on_aboutdialog_response(self, widget, response):
        """
        This function runs when the about dialog is closed with the button.
        It hides the about dialog.
        """
        self.ab.hide()

    def on_aboutdialog_close(self):
        """
        This function is run when the about dialog is closed with the x-button
        in the title bar. It hides the about dialog.
        """
        self.ab.hide()

class PrintDialog(object):

    """
    This class handles the signals of the GtkPrintUnixDialog.

    The properties and signals of the Print dialog are set in Glade. This
    class parses the Glade file and controls the signals of the dialog.
    """

    def __init__(self):
        """
        Initializes the Print dialog.

        Loads the Gtk.Builder and parses the Glade file. An instance of the
        Print dialog is created and the signals are connected to this class.
        """
        self.builder = Gtk.Builder()
        self.builder.add_objects_from_file("gui_layout.glade",
            ("printdialog", ""))
        self.pd = self.builder.get_object("printdialog")
        self.builder.connect_signals(self)

    def run(self):
        """
        Runs the GtkPrintUnixDialog.
        """
        self.pd.run()

    def on_printdialog_destroy(self, widget):
        """
        Hides the GtkPrintUnixDialog.
        """
        self.pd.hide()

    def on_printdialog_close(self):
        """
        Hides the GtkPrintUnixDialog.
        """
        self.pd.hide()

    def on_printdialog_response(self, widget, response):
        """
        Catches the response of the GtkPrintUnixDialog.
        """
        if response == Gtk.ResponseType.OK:
            pass
        elif response == Gtk.ResponseType.CANCEL:
            pass

class StereonetProperties(object):

    """
    This class handles the signals of the plot properties dialog.
    """

    def __init__(self, settings, redraw_function):
        """
        Initializes the plot-properties dialog. Connects the Gtk.Builder
        loads the current settings and connects the signals of the dialog
        window.
        """
        self.builder = Gtk.Builder()
        self.builder.add_objects_from_file("gui_layout.glade",
            ("stereonet_properties_dialog", "adjustment_pixel_density"))
        self.spd = self.builder.get_object("stereonet_properties_dialog")
        self.spinbutton_pixel_density = \
                    self.builder.get_object("spinbutton_pixel_density")
        self.adjustment_pixel_density = \
                    self.builder.get_object("adjustment_pixel_density")
        self.radio_schmidt = self.builder.get_object("radiobutton_schmidt")
        self.radio_wulff = self.builder.get_object("radiobutton_wulff")
        self.checkbutton_draw_grid = \
                    self.builder.get_object("checkbutton_draw_grid")
        self.checkbutton_draw_legend = \
                    self.builder.get_object("checkbutton_draw_legend")
        self.colorbutton_canvas = \
                    self.builder.get_object("colorbutton_canvas")
        
        self.redraw = redraw_function
        self.changes = []
        self.settings = settings
        self.adjustment_pixel_density.set_value(
                                        self.settings.get_pixel_density())
        self.colorbutton_canvas.set_color(self.settings.get_canvas_rgba())
        if self.settings.get_projection_state() == True:
            self.radio_schmidt.set_active(True)
        else:
            self.radio_wulff.set_active(True)
        self.checkbutton_draw_grid.set_active(
                                    self.settings.get_draw_grid_state())
        self.checkbutton_draw_legend.set_active(
                                    self.settings.get_draw_legend())
        self.builder.connect_signals(self)

    def on_spinbutton_pixel_density_value_changed(self, spinbutton):
        """
        Triggered when the spinbutton for the pixel density is changed. Queues
        up the new value in the list of changes.
        """
        new_pixel_density = spinbutton.get_value()
        self.changes.append(lambda: self.settings.set_pixel_density(
                            new_pixel_density))

    def on_button_apply_clicked(self, widget):
        """
        Triggered when "Apply" is clicked in the "properties"-dialog. This
        means that the list of changes is applied one by one. Then the dialog
        is hidden and triggers a redraw of the plot.
        """
        for change in self.changes:
            change()
        self.spd.hide()
        self.redraw(checkout_canvas = True)

    def on_radiobutton_schmidt_toggled(self, button):
        """
        Triggered when the radiobutton for equal area projections is toggled
        on or off. Because there are only 2 radiobuttons, a "False" implies
        that the equal angle button was selected. The function queues up a
        lambda function in the "changes"-list.
        """
        if button.get_active():
            state = True
        else:
            state = False
        self.changes.append(lambda: self.settings.set_projection_state(state))

    def on_checkbutton_draw_grid_toggled(self, checkbutton):
        """
        Triggered when the checkbutton for the grid drawing is toggled. Queues
        up the new state in the list of changes.
        """
        state = checkbutton.get_active()
        self.changes.append(lambda: self.settings.set_draw_grid_state(state))

    def on_checkbutton_draw_legend_toggled(self, checkbutton):
        """
        Triggered when the checkbutton for the legend drawing is toggled. Queues
        up the new state in the list of changes.
        """
        state = checkbutton.get_active()
        self.changes.append(lambda: self.settings.set_draw_legend(state))

    def run(self):
        """
        Triggered when the dialog is run from the main window. An instance of
        the dialog was already initialized and appears by calling this function.
        """
        self.spd.run()

    def on_stereonet_properties_dialog_close(self, widget):
        """
        This function is triggered when the dialog is closed. It hides the
        dialog.
        """
        self.spd.hide()

    def on_stereonet_properties_dialog_response(self, widget, response):
        """
        This function catches the response of the dialog.
        """
        self.spd.hide()

    def on_button_settings_cancel_clicked(self, widget):
        """
        Triggered when Cancel is clicked. Hides the dialog.
        """
        self.spd.hide()

    def on_colorbutton_canvas_color_set(self, colorbutton):
        """
        Triggered when a new color is chosen for the canvas.
        """
        rgba = colorbutton.get_rgba()
        rgb_str = rgba.to_string()
        red, green, blue = rgb_str[4:-1].split(",")
        color_list = [int(red)/255, int(green)/255, int(blue)/255]
        new_canvas_color = colors.rgb2hex(color_list)
        self.changes.append(
                lambda: self.settings.set_canvas_color(new_canvas_color))

class LayerProperties(object):

    """
    This class intializes the layer properties dialog and handles its signals.
    The init method requires a layer object, so the changes can be applied and
    a function from the main loop that redraws the plot after changes are
    applied.
    """

    def __init__(self, layer, redraw_plot):
        """
        Initializes the Gtk.Builder and loads the about dialog from glade file.
        The builder creates and instance of the about dialog and connects
        the signals.        
        """
        self.builder = Gtk.Builder()
        self.builder.add_objects_from_file("gui_layout.glade",
            ("dialog_layer_properties", "liststore_line_style",
            "adjustment_line_width", "liststore_capstyle",
            "liststore_marker_style", "adjustment_marker_size",
            "adjustment_edge_width", "adjustment_pole_size",
            "adjustment_pole_edge_width", "adjustment_rose_spacing",
            "adjustment_rose_bottom", "adjustment_contour_resolution",
            "liststore_colormaps", "liststore_contour_method",
            "adjustment_contour_sigma", "adjustment_contour_label_size"))
        self.layer = layer
        self.redraw = redraw_plot
        self.changes = []
        self.dialog = self.builder.get_object("dialog_layer_properties")
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
        self.load_contour_properties()
        self.load_rose_properties()
        self.hide_gui_elements()
        self.builder.connect_signals(self)

    def load_circle_properties(self):
        """
        Load default settings for great- and small circles
        """
        self.checkbutton_render_gcircles = \
                        self.builder.get_object("checkbutton_render_gcircles")
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
        self.checkbutton_render_gcircles.set_active(
                              self.layer.get_render_gcircles())
        self.colorbutton_line.set_color(self.layer.get_rgba())
        self.adjustment_line_width.set_value(self.layer.get_line_width())
        self.combobox_line_style.set_active(
                              self.line_style_dict[self.layer.get_line_style()])
        self.combobox_capstyle.set_active(
                              self.capstyle_dict[self.layer.get_capstyle()])

    def load_pole_properties(self):
        """
        Load default settings for pole points
        """
        self.checkbutton_render_poles = \
                        self.builder.get_object("checkbutton_render_poles")
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
        self.checkbutton_render_poles.set_active(self.layer.get_render_poles())
        self.colorbutton_pole_fill.set_color(self.layer.get_pole_rgba())
        self.colorbutton_pole_edge_color.set_color(
                            self.layer.get_pole_edge_rgba())
        self.adjustment_pole_size.set_value(
                            self.layer.get_pole_size())
        self.adjustment_pole_edge_width.set_value(
                            self.layer.get_pole_edge_width())
        self.combobox_pole_style.set_active(
                            self.marker_style_dict[self.layer.get_pole_style()])

    def load_linear_properties(self):
        """
        Load the current settings for linear markers
        """
        self.checkbutton_render_linears = \
                        self.builder.get_object("checkbutton_render_linears")
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
        self.checkbutton_render_linears.set_active(
                        self.marker_style_dict[self.layer.get_pole_style()])
        self.combobox_marker_style.set_active(
                        self.marker_style_dict[self.layer.get_marker_style()])
        self.adjustment_marker_size.set_value(self.layer.get_marker_size())
        self.colorbutton_marker.set_color(self.layer.get_marker_rgba())
        self.colorbutton_marker_edge.set_color(
                                self.layer.get_marker_edge_rgba())
        self.adjustment_marker_edge_width.set_value(
                                self.layer.get_marker_edge_width())

    def load_contour_properties(self):
        """
        Load the current settings for contours
        """
        self.checkbutton_draw_contour_fills = \
                       self.builder.get_object("checkbutton_draw_contour_fills")
        self.checkbutton_draw_contour_lines = \
                       self.builder.get_object("checkbutton_draw_contour_lines")
        self.radiobutton_contour_poles = \
                        self.builder.get_object("radiobutton_contour_poles")
        self.radiobutton_contour_linears = \
                        self.builder.get_object("radiobutton_contour_linears")
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
        self.checkbutton_draw_contour_labels = \
                      self.builder.get_object("checkbutton_draw_contour_labels")
        self.spinbutton_contour_label_size = \
                        self.builder.get_object("spinbutton_contour_label_size")
        self.adjustment_contour_label_size = \
                        self.builder.get_object("adjustment_contour_label_size")
        self.radiobutton_use_color = \
                        self.builder.get_object("radiobutton_use_color")
        self.radiobutton_use_colormap = \
                        self.builder.get_object("radiobutton_use_colormap")
        self.colorbutton_contour_line_color = \
                        self.builder.get_object("colorbutton_contour_line_color")
        self.checkbutton_draw_contour_fills.set_active(
                                self.layer.get_draw_contour_fills())
        self.checkbutton_draw_contour_lines.set_active(
                                self.layer.get_draw_contour_lines())
        self.checkbutton_draw_contour_labels.set_active(
                                self.layer.get_draw_contour_labels())
        if self.layer.get_render_pole_contours() == True:
            self.radiobutton_contour_poles.set_active(True)
        else:
            self.radiobutton_contour_linears.set_active(True)
        
        if self.layer.get_use_line_color() == True:
            self.radiobutton_use_color.set_active(True)
        else:
            self.radiobutton_use_colormap.set_active(True)

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
        """
        self.notebook = \
                        self.builder.get_object("notebook1")
        self.box_contour_faultplanes = \
                        self.builder.get_object("box_contour_faultplanes")
        layertype = self.layer.get_layer_type()
        if layertype == "line":
            self.notebook.get_nth_page(0).hide()
            self.notebook.get_nth_page(1).hide()
            self.box_contour_faultplanes.hide()
        elif layertype == "plane":
            self.notebook.get_nth_page(2).hide()
            self.box_contour_faultplanes.hide()
        elif layertype == "smallcircle":
            self.notebook.get_nth_page(1).hide()
            self.notebook.get_nth_page(2).hide()
            self.notebook.get_nth_page(3).hide()
            self.notebook.get_nth_page(4).hide()
            self.box_contour_faultplanes.hide()

    def on_checkbutton_render_linears_toggled(self, checkbutton):
        """
        Triggered when the checkbutton for linears is changed. Queues up the
        new state in the list of changes.
        """
        new_checkbutton_linears_state = checkbutton.get_active()
        self.changes.append(lambda: self.layer.set_render_linears(
                                            new_checkbutton_linears_state))

    def on_entry_layer_name_changed(self, entry):
        """
        Triggered when the layer name is changed. Reads out the text buffer and
        stores the name as a string in a temporary variable.
        """
        buffer_obj = entry.get_buffer()
        new_label = buffer_obj.get_text()
        self.changes.append(lambda: self.layer.set_label(new_label))

    def on_checkbutton_render_gcircles_toggled(self, checkbutton):
        """
        Triggered when the checkbutton for great circles is changed. Sets
        self.properties_changed as True. Gets the new state from the widget
        and stores it in a temporary variable.
        """
        new_checkbutton_gcircles_state = checkbutton.get_active()
        self.changes.append(lambda: self.layer.set_render_gcircles(
                                            new_checkbutton_gcircles_state))

    def on_checkbutton_render_poles_toggled(self, checkbutton):
        """
        Triggered when the state of the checkbutton for poles is changed. Sets
        self.properties_changed as True. Gets the new state from the widget
        and stores it in a temporary variable.
        """
        new_checkbutton_poles_state = checkbutton.get_active()
        self.changes.append(lambda: self.layer.set_render_poles(
                                            new_checkbutton_poles_state))

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
        self.dialog.hide()

    def on_button_layerproperties_apply_clicked(self, widget):
        """
        When apply is pressed this function applies all changes and closes
        the dialog window.
        """
        for change in self.changes:
            change()
        
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

    def on_checkbutton_draw_contour_fills_toggled(self, checkbutton):
        """
        Triggered when the state of the checkbutton for rendering contour fills
        is toggled. Queues up the new state in the list of changes.
        """
        draw_contour_fills_state = checkbutton.get_active()
        self.changes.append(
            lambda: self.layer.set_draw_contour_fills(draw_contour_fills_state))

    def on_checkbutton_draw_contour_lines_toggled(self, checkbutton):
        """
        Triggered when the state of the checkbutton for rendering contour lines
        is toggled. Queues up the new state in the list of changes.
        """
        draw_contour_lines_state = checkbutton.get_active()
        self.changes.append(
            lambda: self.layer.set_draw_contour_lines(draw_contour_lines_state))

    def on_radiobutton_contour_poles_toggled(self, radiobutton):
        """
        Triggered when the radiobutton-group for contouring poles and contouring
        lines is toggled. Because there are only two options if one is True
        the other one is False.
        """
        if radiobutton.get_active():
            state = True
        else:
            state = False
        self.changes.append(
                    lambda: self.layer.set_render_pole_contours(state))
        self.changes.append(
                    lambda: self.layer.set_render_line_contours(not state))

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

    def on_checkbutton_draw_contour_labels_toggled(self, checkbutton):
        """
        Triggerd when the checkbutton to draw contour labels is toggeled.
        Queues up the new state in the list of changes.
        """
        draw_contour_labels = checkbutton.get_active()
        self.changes.append(
            lambda: self.layer.set_draw_contour_labels(draw_contour_labels))

    def on_spinbutton_contour_label_size_value_changed(self, spinbutton):
        """
        Triggered when the font size for contour labels is changed. The new
        value is queued up in the list of changes.
        """
        label_size = int(spinbutton.get_value())
        self.changes.append(
             lambda: self.layer.set_contour_label_size(label_size))

    def on_radiobutton_use_color_toggled(self, radiobutton):
        """
        Triggered when the radiobutton to use colors is toggled on or off.
        Because there are only two buttons in the group, it is not necessary
        to have functions for the other buttons. Queues up the new value
        in the list of changes.
        """
        if radiobutton.get_active():
            state = True
        else:
            state = False
        self.changes.append(lambda: self.layer.set_use_line_color(state))

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

class FileChooserParse(object):

    """
    This class handles the actions of the filechooserdialog that selects
    files for text parsing.
    """

    def __init__(self, run_file_parser):
        self.builder = Gtk.Builder()
        self.builder.add_objects_from_file("gui_layout.glade",
            ("filechooserdialog_parse", "filefilter_parse"))
        self.dialog = self.builder.get_object("filechooserdialog_parse")
        self.filefilters = self.builder.get_object("filefilter_parse")
        self.filefilters.set_name("Text Files")
        self.dialog.add_filter(self.filefilters)
        self.run_file_parser = run_file_parser
        self.builder.connect_signals(self)

    def run(self):
        """
        This function is run when the filechooserdialog for text parsing
        is called from the main window. It runs the dialog.
        """
        self.dialog.run()

    def on_filechooserdialog_parse_destroy(self, widget):
        """
        This function is run when the filechooserdialog is destroyed. Hides
        the dialog.
        """
        self.dialog.hide()

    def on_filechooserdialog_parse_close(self, widget):
        """
        Triggered when the filechooserdialog is closed. Hides the dialog.
        """
        self.dialog.hide()

    def on_filechooserdialog_parse_response(self, widget, response):
        """
        Triggered when the filechooserdialog sends a response.
        """
        if response == -4:
            self.dialog.hide()

    def on_button_open_clicked(self, widget):
        """
        Triggered when "open" is clicked.
        """
        text_file = self.dialog.get_filename()
        self.dialog.hide()
        self.run_file_parser(text_file)

    def on_button_cancel_clicked(self, widget):
        """
        Triggered when "cancel" is clicked. Hides the dialog.
        """
        self.dialog.hide()
