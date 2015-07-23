#!/usr/bin/python3

"""
This module contains dialog windows.

Each dialog window has its own class that controls its behaviour. This module
stores the AboutDialog-, StereonetProperties-, LayerProperties-,
and FileChooserParse-class.
"""

from gi.repository import Gtk
import matplotlib.colors as colors
import os


class AboutDialog(object):

    """
    This class controls the about dialog and handles its signals.

    The layout and content of the About Dialog is stored in the Glade file.
    This class parses the glade file for the dialog, and connects the signals
    that are declared in Glade.
    """

    def __init__(self, main_window):
        """
        Initializes the AboutDialog.

        Loads the Gtk.Builder and parses the Glade file. Then the signals, that
        are declared in the Glade file are connected to this class.
        """
        self.builder = Gtk.Builder()
        script_dir = os.path.dirname(__file__)
        rel_path = "gui_layout.glade"
        abs_path = os.path.join(script_dir, rel_path)
        self.builder.add_objects_from_file(abs_path,
            ("aboutdialog", ""))
        self.ab = self.builder.get_object("aboutdialog")
        self.ab.set_transient_for(main_window)
        self.builder.connect_signals(self)

    def run(self):
        """
        Runs the dialog.

        This function is run when the about dialog is called from the main
        window. It shows the about dialog.
        """
        self.ab.run()

    def on_aboutdialog_response(self, widget, response):
        # pylint: disable=unused-argument
        """
        The response of the AboutDialog hides the dialog.

        This function runs when the about dialog is closed with the button.
        It hides the about dialog.
        """
        self.ab.hide()

    def on_aboutdialog_close(self):
        """
        Triggered when the AboutDialog is closed. Hides the Dialog.

        This function is run when the about dialog is closed with the x-button
        in the title bar. It hides the about dialog.
        """
        self.ab.hide()


class StereonetProperties(object):

    """
    This class handles the signals of the plot properties dialog.

    The plot-properties dialog contains options to change the appearance
    of the the plot. Those are are all settings that are not individual to
    a data-layer. This class loads the dialog from the Glade-file and
    connects all the signals defined in the that file.
    """

    def __init__(self, settings, redraw_function, main_window, change_night_mode):
        """
        Initializes the plot-properties dialog.

        Initializes the plot-properties dialog. Connects the Gtk.Builder
        loads the current settings and connects the signals of the dialog
        window.
        """
        self.builder = Gtk.Builder()
        script_dir = os.path.dirname(__file__)
        rel_path = "gui_layout.glade"
        abs_path = os.path.join(script_dir, rel_path)
        self.builder.add_objects_from_file(abs_path,
            ("stereonet_properties_dialog", "adjustment_pixel_density"))
        self.spd = self.builder.get_object("stereonet_properties_dialog")
        self.spd.set_transient_for(main_window)
        self.spinbutton_pixel_density = \
                    self.builder.get_object("spinbutton_pixel_density")
        self.adjustment_pixel_density = \
                    self.builder.get_object("adjustment_pixel_density")
        self.switch_equal_area = self.builder.get_object("switch_equal_area")
        self.switch_draw_grid = \
                    self.builder.get_object("switch_draw_grid")
        self.switch_draw_legend = \
                    self.builder.get_object("switch_draw_legend")
        self.colorbutton_canvas = \
                    self.builder.get_object("colorbutton_canvas")
        self.radio_north = \
                    self.builder.get_object("radiobutton_north")
        self.radio_degrees = \
                    self.builder.get_object("radiobutton_degrees")
        self.switch_show_cross = \
                    self.builder.get_object("switch_show_cross")
        self.switch_highlight = self.builder.get_object("switch_highlight")
        self.switch_night_mode = self.builder.get_object("switch_night_mode")

        self.redraw = redraw_function
        self.change_night_mode = change_night_mode
        self.changes = []
        self.settings = settings
        self.switch_equal_area.set_active(self.settings.get_projection_state())
        self.adjustment_pixel_density.\
            set_value(self.settings.get_pixel_density())
        self.colorbutton_canvas.set_color(self.settings.get_canvas_rgba())
        self.switch_draw_grid.\
            set_active(self.settings.get_draw_grid_state())
        self.switch_draw_legend.\
            set_active(self.settings.get_draw_legend())
        if self.settings.get_show_north() == True:
            self.radio_north.set_active(True)
        else:
            self.radio_degrees.set_active(True)
        self.switch_show_cross.set_active(self.settings.get_show_cross())
        self.switch_highlight.set_active(self.settings.get_highlight())
        self.switch_night_mode.set_active(self.settings.get_night_mode())
        self.builder.connect_signals(self)

    def on_spinbutton_pixel_density_value_changed(self, spinbutton):
        # pylint: disable=unused-argument
        """
        Queues up the new pixel-density setting.

        Triggered when the spinbutton for the pixel density is changed. Queues
        up the new value in the list of changes.
        """
        new_pixel_density = spinbutton.get_value()
        self.changes.append(lambda: self.settings.set_pixel_density(
                            new_pixel_density))

    def on_button_apply_clicked(self, widget):
        # pylint: disable=unused-argument
        """
        Applies all the changes set in the dialog and hides the dialog.

        Triggered when "Apply" is clicked in the "properties"-dialog. This
        means that the list of changes is applied one by one. Then the dialog
        is hidden and triggers a redraw of the plot.
        """
        for change in self.changes:
            change()
        self.spd.hide()
        self.redraw(checkout_canvas=True)

    def on_switch_equal_area_state_set(self, switch, state):
        # pylint: disable=unused-argument
        """
        Queues up the new projection-setting of the stereonet.

        Triggered when the equal-area switch is toggled. True means that
        the projection is equal area. False means the projection is equal
        angle.
        """
        self.changes.append(lambda: self.settings.set_projection_state(state))

    def on_switch_draw_grid_state_set(self, switch, state):
        # pylint: disable=unused-argument
        """
        Queues up the new grid-drawing setting in the list of changes.

        Triggered when the switch for the grid drawing is toggled. Queues
        up the new state in the list of changes.
        """
        self.changes.append(lambda: self.settings.set_draw_grid_state(state))

    def on_switch_draw_legend_state_set(self, switch, state):
        # pylint: disable=unused-argument
        """
        Queues up the new legend-drawing setting.

        Triggered when the switch for the legend drawing is toggled. Queues
        up the new state in the list of changes.
        """
        self.changes.append(lambda: self.settings.set_draw_legend(state))

    def run(self):
        """
        Runs the dialog.

        Triggered when the dialog is run from the main window. An instance of
        the dialog was already initialized and appears by calling this function.
        """
        self.spd.run()

    def on_stereonet_properties_dialog_close(self, widget):
        # pylint: disable=unused-argument
        """
        Hides the dialog.

        This function is triggered when the dialog is closed. It hides the
        dialog.
        """
        self.spd.hide()

    def on_stereonet_properties_dialog_response(self, widget, response):
        # pylint: disable=unused-argument
        """
        Triggered by the dialog response. Hides the dialog.

        This method is executed when the response of the dialog is triggered.
        It hides the dialog.
        """
        self.spd.hide()

    def on_button_settings_cancel_clicked(self, widget):
        # pylint: disable=unused-argument
        """
        Hides the dialog.

        Triggered when Cancel is clicked. Hides the dialog.
        """
        self.spd.hide()

    def on_colorbutton_canvas_color_set(self, colorbutton):
        # pylint: disable=unused-argument
        """
        Queues up the new color of the canvas.

        Triggered when a new color is chosen for the canvas.
        """
        rgba = colorbutton.get_rgba()
        rgb_str = rgba.to_string()
        red, green, blue = rgb_str[4:-1].split(",")
        color_list = [int(red)/255, int(green)/255, int(blue)/255]
        new_canvas_color = colors.rgb2hex(color_list)
        self.changes.append(
                lambda: self.settings.set_canvas_color(new_canvas_color))

    def on_radiobutton_north_toggled(self, radiobutton):
        # pylint: disable=unused-argument
        """
        Queues up the new setting for the North symbol.

        Triggered when the radio-button-group for the North symbol or 
        degree symbols is toggled. True means that the North symbol will be
        drawn. False means that the degree symbols will be drawn.
        """
        if radiobutton.get_active():
            state = True
        else:
            state = False
        self.changes.append(lambda: self.settings.set_show_north(state))

    def on_switch_show_cross_state_set(self, switch, state):
        # pylint: disable=unused-argument
        """
        Queues up the new setting, if the center cross should be drawn

        Triggered when the switch for the center cross is toggled.
        Queues up a boolean value. True means that the cross is drawn. False
        means it is not drawn.
        """
        self.changes.append(lambda: self.settings.set_show_cross(state))

    def on_switch_highlight_state_set(self, switch, state):
        # pylint: disable=unused-argument
        """
        Queues up the new setting, if selection should be highlighted.

        Triggered when the switch for selection highlighting is toggled.
        Queues up a boolean value. True means that highlighting is on. False
        means it is off.
        """
        self.changes.append(lambda: self.settings.set_highlight(state))

    def on_switch_night_mode_state_set(self, switch, state):
        # pylint: disable=unused-argument
        """
        Queues up the new setting, if night mode should be used.

        Triggered when the switch for night mode is toggled.
        Queues up a boolean value. True means that the interface will
        appear dark. False means it will be the systems default.
        """
        self.changes.append(lambda: self.settings.set_night_mode(state))
        self.changes.append(lambda: self.change_night_mode())


class FileChooserParse(object):

    """
    Sets up and handles all the signals of the FileChooser for parsing.

    This class handles the actions of the filechooserdialog that selects
    files for text parsing.
    """

    def __init__(self, run_file_parser, main_window):
        self.builder = Gtk.Builder()
        script_dir = os.path.dirname(__file__)
        rel_path = "gui_layout.glade"
        abs_path = os.path.join(script_dir, rel_path)
        self.builder.add_objects_from_file(abs_path,
            ("filechooserdialog_parse", "filefilter_parse"))
        self.dialog = self.builder.get_object("filechooserdialog_parse")
        self.dialog.set_transient_for(main_window)
        self.filefilters = self.builder.get_object("filefilter_parse")
        self.filefilters.set_name(_("Text Files"))
        self.dialog.add_filter(self.filefilters)
        self.run_file_parser = run_file_parser
        self.builder.connect_signals(self)

    def run(self):
        """
        Runs the dialog.

        This function is run when the filechooserdialog for text parsing
        is called from the main window. It runs the dialog.
        """
        self.dialog.run()

    def on_filechooserdialog_parse_destroy(self, widget):
        # pylint: disable=unused-argument
        """
        Hides the dialog.

        This function is run when the filechooserdialog is destroyed. Hides
        the dialog.
        """
        self.dialog.hide()

    def on_filechooserdialog_parse_close(self, widget):
        # pylint: disable=unused-argument
        """
        Hides the dialog.

        Triggered when the filechooserdialog is closed. Hides the dialog.
        """
        self.dialog.hide()

    def on_filechooserdialog_parse_response(self, widget, response):
        # pylint: disable=unused-argument
        """
        Hides the dialog.

        Triggered when the filechooserdialog sends a response.
        """
        if response == -4:
            self.dialog.hide()

    def on_button_open_clicked(self, widget):
        # pylint: disable=unused-argument
        """
        Opens a file and passes the file location back to the MainWindow-class.

        Triggered when "open" is clicked.
        """
        text_file = self.dialog.get_filename()
        self.dialog.hide()
        self.run_file_parser(text_file)

    def on_button_cancel_clicked(self, widget):
        # pylint: disable=unused-argument
        """
        Hides the dialog.

        Triggered when "cancel" is clicked. Hides the dialog.
        """
        self.dialog.hide()


class FileChooserExport(object):

    """
    Sets up and handles the signals of the FileChooser for exporting data.

    This class handles the actions of the filechooserdialog that is used
    to export data.
    """

    def __init__(self, export_data, main_window):
        self.builder = Gtk.Builder()
        self.export_data = export_data
        script_dir = os.path.dirname(__file__)
        rel_path = "gui_layout.glade"
        abs_path = os.path.join(script_dir, rel_path)
        self.builder.add_objects_from_file(abs_path,
            ("filechooserdialog_export", ""))
        self.dialog = self.builder.get_object("filechooserdialog_export")
        self.dialog.set_transient_for(main_window)
        self.builder.connect_signals(self)

    def run(self):
        """
        Runs the dialog.

        This function is run when the filechooserdialog for export is called
        from the main window.
        """
        self.dialog.run()

    def on_filechooserdialog_export_close(self, widget):
        # pylint: disable=unused-argument
        """
        Hides the FileChooserExport dialog.

        Triggered when the FileChooserExport dialog is closed. Hides the dialog.
        """
        self.dialog.hide()

    def on_filechooserdialog_export_response(self, widget, response):
        # pylint: disable=unused-argument
        """
        Hides the FileChooserExport dialog.

        Triggered when the FileChooserExport dialog sends a response.
        """
        if response == -4:
            self.dialog.hide()

    def on_filechooserdialog_export_destroy(self, widget):
        # pylint: disable=unused-argument
        """
        Hides the FileChooserExport dialog.

        This function is run when the FileChooserExport dialog is destroyed.
        Hides the dialog.
        """
        self.dialog.hide()

    def on_button_cancel_export_clicked(self, button):
        # pylint: disable=unused-argument
        """
        Hides the FileChooserExport dialog.

        Triggered when "cancel" is clicked. Hides the dialog.
        """
        self.dialog.hide()

    def on_button_export_data_clicked(self, button):
        # pylint: disable=unused-argument
        """
        Passes file location to the export_data function and closes the dialog.

        The user should navigate to a desired location and type a filename. The
        filename is called and passes to the MainWindow's export_data function.
        The dialog is hidden afterwards.
        """
        self.filename = self.dialog.get_filename()
        if os.path.exists(self.filename) == True:
            overwrite = OverwriteDialog(self.call_overwrite, self.dialog)
            overwrite.run()
        else:
            self.export_data(self.filename)
            self.dialog.hide()

    def call_overwrite(self):
        """
        Overwrites the existing file.

        The function calls the export_data function of the MainWindow class,
        overwritting the exisisting file, that needs to be passed to that
        method. Then the dialog is hidden.
        """
        self.export_data(self.filename)
        self.dialog.hide()


class OverwriteDialog(object):

    """
    Sets up and handles the signals of the OverWriteDialog for exporting data.

    If a file already exists this dialog confirms if the file should be
    overwritten. This class handles all the signals of the dialog.
    """

    def __init__(self, call_overwrite, export_dialog):
        self.builder = Gtk.Builder()
        self.call_overwrite = call_overwrite
        script_dir = os.path.dirname(__file__)
        rel_path = "gui_layout.glade"
        abs_path = os.path.join(script_dir, rel_path)
        self.builder.add_objects_from_file(abs_path,
            ("dialog_overwrite", ""))
        self.dialog = self.builder.get_object("dialog_overwrite")
        self.dialog.set_transient_for(export_dialog)
        self.builder.connect_signals(self)

    def run(self):
        """
        Runs the dialog.

        This function is run when the OverWriteDialog is called from another
        dialog.
        """
        self.dialog.run()

    def on_button_cancel_overwrite_clicked(self, button):
        # pylint: disable=unused-argument
        """
        Cancels the overwrite and returns to the FileExportDialog.

        When the user clicks on cancel the OverWriteDialog is closed. The
        focus returns to the FileChooserDialog of the FileExportDialog class.
        """
        self.dialog.hide()

    def on_button_overwrite_clicked(self, button):
        # pylint: disable=unused-argument
        """
        Overwrites the exisisting file.

        When the user clicks on overwrite, the OverWriteDialog calls the
        call_overwrite method of the FileChooserDialog class. This results in the
        existing file being overwritten. Then the dialog is closed.
        """
        self.call_overwrite()
        self.dialog.hide()

class FileChooserSave(object):

    """
    Sets up and handles the signals of the FileChooser for saving the project.

    This class handles the actions of the filechooserdialog that is used
    to save the project.
    """

    def __init__(self, main_window, data):
        self.builder = Gtk.Builder()
        self.data = data
        script_dir = os.path.dirname(__file__)
        rel_path = "gui_layout.glade"
        abs_path = os.path.join(script_dir, rel_path)
        self.builder.add_objects_from_file(abs_path,
            ("filechooserdialog_save", ""))
        self.dialog = self.builder.get_object("filechooserdialog_save")
        self.dialog.set_transient_for(main_window)
        self.builder.connect_signals(self)

    def run(self):
        """
        Runs the dialog.

        This function is run when the filechooserdialog for saving is called
        from the main window.
        """
        self.dialog.run()

    def on_filechooserdialog_save_close(self, widget):
        # pylint: disable=unused-argument
        """
        Hides the FileChooserSave dialog.

        Triggered when the FileChooserSave dialog is closed. Hides the dialog.
        """
        self.dialog.hide()

    def on_filechooserdialog_save_response(self, widget, response):
        # pylint: disable=unused-argument
        """
        Hides the FileChooserSave dialog.

        Triggered when the FileChooserSave dialog sends a response.
        """
        if response == -4:
            self.dialog.hide()

    def on_filechooserdialog_save_destroy(self, widget):
        # pylint: disable=unused-argument
        """
        Hides the FileChooserSave dialog.

        This function is run when the FileChooserSave dialog is destroyed.
        Hides the dialog.
        """
        self.dialog.hide()

    def on_button_cancel_save_clicked(self, button):
        # pylint: disable=unused-argument
        """
        Hides the FileChooserSave dialog.

        Triggered when "cancel" is clicked. Hides the dialog.
        """
        self.dialog.hide()

    def on_button_confirm_save_clicked(self, button):
        # pylint: disable=unused-argument
        """
        Saves the project.

        If the file already exists a dialog will confirm the overwrite.
        """
        self.filename = self.dialog.get_filename()
        if self.filename[-5:] != ".json":
            self.filename = self.filename + ".json"
        if os.path.exists(self.filename) == True:
            overwrite = OverwriteDialog(self.write_data, self.dialog)
            overwrite.run()
        else:
            self.write_data()
            self.dialog.hide()

    def write_data(self):
        """
        Writes the data to the file.

        Opens the file the user has inputted and writes the data to that file.
        """
        with open(self.filename, "w") as new_file:
            new_file.write(self.data)
        self.dialog.hide()


class FileChooserOpen(object):

    """
    Sets up and handles all the signals of the FileChooser for opening a project

    This class handles the actions of the filechooserdialog that selects a
    project file and returns the file to the main window.
    """

    def __init__(self, main_window, open_project):
        self.builder = Gtk.Builder()
        script_dir = os.path.dirname(__file__)
        rel_path = "gui_layout.glade"
        abs_path = os.path.join(script_dir, rel_path)
        self.builder.add_objects_from_file(abs_path,
            ("filechooserdialog_open", ""))
        self.dialog = self.builder.get_object("filechooserdialog_open")
        self.dialog.set_transient_for(main_window)
        filter_json = Gtk.FileFilter()
        filter_json.add_pattern("*.json")
        filter_json.set_name("JSON")
        self.dialog.add_filter(filter_json)
        filter_all = Gtk.FileFilter()
        filter_all.add_pattern("*")
        filter_all.set_name(_("All Files"))
        self.dialog.add_filter(filter_all)
        self.open_project = open_project
        self.builder.connect_signals(self)

    def run(self):
        """
        Runs the dialog.

        This function is run when the filechooserdialog for opening a project
        is called from the main window.
        """
        self.dialog.run()

    def on_filechooserdialog_open_destroy(self, widget):
        # pylint: disable=unused-argument
        """
        Hides the dialog.

        This function is run when the filechooserdialog is destroyed.
        """
        self.dialog.hide()

    def on_filechooserdialog_open_close(self, widget):
        # pylint: disable=unused-argument
        """
        Hides the dialog.

        Triggered when the filechooserdialog is closed.
        """
        self.dialog.hide()

    def on_filechooserdialog_open_response(self, widget, response):
        # pylint: disable=unused-argument
        """
        Hides the dialog.

        Triggered when the filechooserdialog sends a response.
        """
        if response == -4:
            self.dialog.hide()

    def on_button_confirm_open_clicked(self, widget):
        # pylint: disable=unused-argument
        """
        Opens a file and passes the file location back to the main window.

        Triggered when "open" is clicked. The file name is passed to the
        open_project method of the MainWindow class. Then the dialog is hidden.
        """
        json_file = self.dialog.get_filename()
        self.dialog.hide()
        self.open_project(json_file)

    def on_button_cancel_open_clicked(self, widget):
        # pylint: disable=unused-argument
        """
        Hides the dialog.

        Triggered when "cancel" is clicked. Hides the dialog.
        """
        self.dialog.hide()

