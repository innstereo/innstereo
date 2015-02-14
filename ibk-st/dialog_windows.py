#!/usr/bin/python3

from gi.repository import Gtk
import matplotlib.colors as colors

class AboutDialog(object):
    """
    This class intializes the about dialog and handles its signals.
    """
    def __init__(self):
        """
        Initializes the Gtk.Builder and loads the about dialog from glade file.
        The builder creates and instance of the about dialog and connects
        the signals.        
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
    """
    def __init__(self):
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
        
        self.redraw = redraw_function
        self.changes = []
        self.settings = settings

        pixel_density = self.settings.get_pixel_density()
        self.adjustment_pixel_density.set_value(pixel_density)

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
            "adjustment_rose_bottom"))
        self.layer = layer
        self.redraw = redraw_plot
        self.changes = []

        self.notebook = \
                        self.builder.get_object("notebook1")
        self.dialog = \
                        self.builder.get_object("dialog_layer_properties")
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
        self.adjustment_marker_edge_width = \
                        self.builder.get_object("adjustment_edge_width")
        self.spinbutton_edge_width = \
                        self.builder.get_object("spinbutton_edge_width")
        self.checkbutton_render_contours = \
                        self.builder.get_object("checkbutton_render_contours")
        self.checkbutton_render_gcircles = \
                        self.builder.get_object("checkbutton_render_gcircles")
        self.checkbutton_render_poles = \
                        self.builder.get_object("checkbutton_render_poles")
        self.checkbutton_render_linears = \
                        self.builder.get_object("checkbutton_render_linears")
        self.colorbutton_pole_fill = \
                        self.builder.get_object("colorbutton_pole_fill")
        self.colorbutton_pole_edge_color = \
                        self.builder.get_object("colorbutton_pole_edge_color")
        self.spinbutton_pole_size = \
                        self.builder.get_object("spinbutton_pole_size")
        self.spinbutton_pole_edge_width = \
                        self.builder.get_object("spinbutton_pole_edge_width")
        self.combobox_pole_style = \
                        self.builder.get_object("combobox_pole_style")
        self.adjustment_pole_size = \
                        self.builder.get_object("adjustment_pole_size")
        self.adjustment_pole_edge_width = \
                        self.builder.get_object("adjustment_pole_edge_width")
        self.spinbutton_rose_spacing = \
                        self.builder.get_object("spinbutton_rose_spacing")
        self.adjustment_rose_spacing = \
                        self.builder.get_object("adjustment_rose_spacing")
        self.spinbutton_rose_bottom = \
                        self.builder.get_object("spinbutton_rose_bottom")
        self.adjustment_rose_bottom = \
                        self.builder.get_object("adjustment_rose_bottom")

        self.colorbutton_line.set_color(self.layer.get_rgba())

        line_style = layer.get_line_style()
        line_style_dict = {"-": 0, "--": 1, "-.": 2, ":": 3}
        self.combobox_line_style.set_active(line_style_dict[line_style])
        
        line_width = layer.get_line_width()
        self.adjustment_line_width.set_value(line_width)

        capstyle = layer.get_capstyle()
        capstyle_dict = {"butt": 0, "round": 1, "projecting": 2}
        self.combobox_capstyle.set_active(capstyle_dict[capstyle])

        marker_style_dict = {".": 0, ",": 1, "o": 2, "v": 3, "^": 4, "<": 5,
                            ">": 6, "s": 7, "8": 8, "p": 9, "*": 10, "h": 11,
                            "H": 12, "+": 13, "x": 14, "D": 15, "d": 16,
                            "|": 17, "_": 18}

        self.combobox_marker_style.set_active(
                                marker_style_dict[layer.get_marker_style()])
        self.adjustment_marker_size.set_value(layer.get_marker_size())
        self.colorbutton_marker.set_color(self.layer.get_marker_rgba())
        self.colorbutton_marker_edge.set_color(
                                self.layer.get_marker_edge_rgba())
        self.adjustment_marker_edge_width.set_value(
                                layer.get_marker_edge_width())

        self.colorbutton_pole_fill.set_color(self.layer.get_pole_rgba())
        self.colorbutton_pole_edge_color.set_color(
                                self.layer.get_pole_edge_rgba())
        self.adjustment_pole_size.set_value(
                                layer.get_pole_size())
        self.adjustment_pole_edge_width.set_value(
                                layer.get_pole_edge_width())
        self.combobox_pole_style.set_active(
                                marker_style_dict[layer.get_pole_style()])

        self.checkbutton_render_contours.set_active(
                                layer.get_render_plane_contours())
        self.checkbutton_render_gcircles.set_active(layer.get_render_gcircles())
        self.checkbutton_render_poles.set_active(layer.get_render_poles())
        self.checkbutton_render_linears.set_active(
                                marker_style_dict[layer.get_pole_style()])
        self.adjustment_rose_spacing.set_value(self.layer.get_rose_spacing())
        self.adjustment_rose_bottom.set_value(self.layer.get_rose_bottom())

        layertype = layer.get_layer_type()
        if layertype == "line":
            self.notebook.get_nth_page(0).hide()
            self.notebook.get_nth_page(1).hide()
            self.notebook.get_nth_page(3).hide()
        elif layertype == "plane":
            self.notebook.get_nth_page(2).hide()
            self.notebook.get_nth_page(4).hide()
        elif layertype == "smallcircle":
            self.notebook.get_nth_page(1).hide()
            self.notebook.get_nth_page(2).hide()
            self.notebook.get_nth_page(3).hide()
            self.notebook.get_nth_page(4).hide()

        self.builder.connect_signals(self)

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
