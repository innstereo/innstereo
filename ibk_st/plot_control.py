#!/usr/bin/python3

from gi.repository import Gtk, Gdk, GdkPixbuf
from matplotlib.figure import Figure
from matplotlib.gridspec import GridSpec
import mplstereonet

class PlotSettings(object):
    def __init__(self):
        """
        Initializes default settings for the figure and stores the instance
        of the Matplotlib-Figure.
        """
        self.folder_icon = Gtk.IconTheme.get_default().load_icon(
            "folder", 16, 0)
        self.default_color = "#0000ff"
        self.default_color_alpha = int("0x{0}ff".format(
            self.default_color[1:]), base=16)
        self.layer_default = GdkPixbuf.Pixbuf.new(
            GdkPixbuf.Colorspace.RGB, True, 8, 16, 16)
        self.layer_default.fill(self.default_color_alpha)
        self.draw_grid = True
        self.equal_area_projection = True
        self.minor_grid_spacing = 2
        self.major_grid_spacing = 10
        self.grid_cutoff_lat = 80
        self.show_north = False
        self.show_center_cross = False
        self.pixel_density = 75
        self.grid_linestyle = "--"
        self.grid_color = "#787878"
        self.grid_width = 0.4
        self.fig = Figure(dpi = self.pixel_density)
        self.draw_legend = True
        self.canvas_color = "#bfbfbf"

    def get_fig(self):
        """
        Returns the Matplotlib-Figure.
        """        
        return self.fig

    def get_inverse_transform(self):
        """
        Returns the inverse transform for the stereonet.
        """
        if self.equal_area_projection == True:
            return mplstereonet.stereonet_transforms.InvertedLambertTransform(
                                0, 0, self.get_pixel_density())
        else:
            return mplstereonet.stereonet_transforms.InvertedStereographicTransform(
                                0, 0, self.get_pixel_density())

    def get_color(self):
        """
        Returns the default color for layers.
        """
        return self.default_color

    def get_draw_grid_state(self):
        """
        Returns if the grid should be drawn.
        """
        return self.draw_grid

    def set_draw_grid_state(self, new_state):
        """
        Sets if the grid should be drawn.
        """
        self.draw_grid = new_state

    def get_folder_icon(self):
        """
        Returns the folder icon used for the group-layer pixbuf.
        """
        return self.folder_icon

    def get_pixel_density(self):
        """
        Returns the pixel density the plot is using.
        """
        return self.pixel_density

    def set_pixel_density(self, new_pixel_density):
        """
        Sets a new pixel density for the plot.
        """
        self.pixel_density = new_pixel_density

    def get_projection(self):
        """
        Returns the projection currently used by the stereonet.
        """
        if self.equal_area_projection == True:
            return "equal_area_stereonet"
        else:
            return "equal_angle_stereonet"

    def get_projection_state(self):
        """
        Returns the projection for the stereonet.
        """
        return self.equal_area_projection

    def set_projection_state(self, new_state):
        """
        Sets a projection state.
        """
        self.equal_area_projection = new_state

    def get_grid_linestyle(self):
        """
        Returns the linestyle of the grid.
        """
        return self.grid_linestyle

    def get_grid_color(self):
        """
        Returns the color of the grid.
        """
        return self.grid_color

    def get_grid_width(self):
        """
        Returns the width of the grid.
        """
        return self.grid_width

    def get_draw_legend(self):
        """
        Returns if the legend should be drawn as a boolean.
        """
        return self.draw_legend

    def set_draw_legend(self, new_state):
        """
        Sets a new state for wheter the legend should be drawn.
        """
        self.draw_legend = new_state

    def get_canvas_color(self):
        """
        Returns the current canvas color in the hex-triplet-format
        (e.g. "#bfbfbf").
        """
        return self.canvas_color

    def get_canvas_rgba(self):
        """
        Returns the RGBA for lines (great and small circles) of the
        current layer.
        __!!__ does not return alpha yet
        """
        rgba = Gdk.RGBA()
        rgba.parse(self.canvas_color)
        return rgba.to_color()

    def set_canvas_color(self, new_color):
        """
        Sets a new canvas color. Requires a string in the hex-triplet-format
        (e.g. "#bfbfbf").
        """
        self.canvas_color = new_color

    def get_stereonet(self):
        """
        Resets the canvas and returns the stereonet axis.
        """
        self.fig.clf()
        self.fig.patch.set_facecolor(self.canvas_color)
        self.fig.set_dpi(self.pixel_density)
        gridspec = GridSpec(1, 1)
        sp_stereo = gridspec.new_subplotspec((0, 0))
        ax_stereo = self.fig.add_subplot(sp_stereo,
                                        projection = self.get_projection())
        return ax_stereo

    def get_stereo_rose(self):
        """
        Resets the canvas and returns the stereonet and rose digarm axis.
        """
        self.fig.clf()
        self.fig.patch.set_facecolor(self.canvas_color)
        self.fig.set_dpi(self.pixel_density)
        gridspec = GridSpec(1, 2)
        sp_stereo = gridspec.new_subplotspec((0, 0),
                                             rowspan = 1, colspan = 1)
        sp_rose = gridspec.new_subplotspec((0, 1),
                                           rowspan = 1, colspan = 1)
        ax_stereo = self.fig.add_subplot(sp_stereo, projection =
                                         self.get_projection())
        ax_rose = self.fig.add_subplot(sp_rose, projection = "northpolar")
        return ax_stereo, ax_rose

    def get_rose_diagram(self):
        """
        Resets the canvas and returns the rose diagram axis.
        """
        self.fig.clf()
        self.fig.patch.set_facecolor(self.canvas_color)
        self.fig.set_dpi(self.pixel_density)
        gridspec = GridSpec(1, 1)
        sp_rose = gridspec.new_subplotspec((0, 0))
        ax_rose = self.fig.add_subplot(sp_rose, projection = "northpolar")
        return ax_rose

    def get_pt_view(self):
        """
        Resets the canvas and return the 3 plots that make up the view
        used for inversion: Stereonet, fluctuation-histogram and mohr-circle.
        """
        self.fig.clf()
        self.fig.patch.set_facecolor(self.canvas_color)
        self.fig.set_dpi(self.pixel_density)
        gridspec = GridSpec(2, 5)
        sp_stereo = gridspec.new_subplotspec((0, 0), colspan=3, rowspan=2)
        sp_fluc = gridspec.new_subplotspec((0, 3), colspan=2)
        sp_mohr = gridspec.new_subplotspec((1, 3), colspan=2)
        ax_stereo = self.fig.add_subplot(sp_stereo, projection =
                                         self.get_projection())
        ax_fluc = self.fig.add_subplot(sp_fluc, aspect = "equal")
        ax_mohr = self.fig.add_subplot(sp_mohr, aspect = "equal")
        return ax_stereo, ax_fluc, ax_mohr
