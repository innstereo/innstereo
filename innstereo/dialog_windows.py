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
