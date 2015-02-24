#!/usr/bin/python3

"""
This module contains the different layers or datasets the program uses.

This module contains the PlaneLayer-class. The other classes inherit most
settings and methods from the PlaneLayer-class. The other classes are
FaulPlaneLayer, LineLayer and SmallCircleLayer. Instances of these classes
are created in the MainWindow-class. During plot-redraws the current styling
of each layer is queried from these classes. The settings are also called when
the layer properties dialog is opened. Changes in the layer properties dialog
are stored in these classes.
"""

from gi.repository import Gdk, GdkPixbuf


class PlaneLayer(object):

    """
    The PlaneLayer class initializes many default settings and methods.

    The settings are currently hardcoded. The methods conists of get-methods,
    to retrieve settings and set-methods to update settings. Colors have an
    additional get-rgba-method.
    """

    def __init__(self, treestore, treeview):
        """
        Initalizes the PlaneLayer class with default settings.

        The settings that are applied here are also set for the layers, that
        inherit from the PlaneLayer class, even if some settings are not used
        for certain layer-types.
        """
        self.data_treestore = treestore
        self.data_treeview = treeview
        self.type = "plane"
        self.label = "Plane layer"

        #Great circle / Small circle properties
        self.render_gcircles = True
        self.line_color = "#0000ff"
        self.line_width = 1.0
        self.line_style = "-"
        self.line_alpha = 1.0
        self.capstyle = "butt"

        #Pole properties
        self.render_poles = False
        self.pole_style = "o"
        self.pole_size = 8.0
        self.pole_fill = "#ff7e00"
        self.pole_edge_color = "#000000"
        self.pole_edge_width = 1.0
        self.pole_alpha = 1.0

        #Linear properties
        self.render_linears = True
        self.marker_style = "o"
        self.marker_size = 8.0
        self.marker_fill = "#1283eb"
        self.marker_edge_color = "#000000"
        self.marker_edge_width = 1.0
        self.marker_alpha = 1.0

        #Rose diagram properties
        self.rose_spacing = 10
        self.rose_bottom = 0

        #Contours
        self.draw_contour_fills = False
        self.draw_contour_lines = False
        self.draw_contour_labels = False
        self.render_plane_contours = False
        self.render_line_contours = True
        self.colormap = "Blues"
        self.contour_resolution = 40
        self.contour_method = "exponential_kamb"
        self.contour_sigma = 3
        self.contour_line_color = "#000000"
        self.contour_use_line_color = True
        self.contour_line_width = 1
        self.contour_line_style = "-"
        self.contour_label_size = 12

    def get_pixbuf(self):
        """
        Takes a color string (format: "#aabbcc") and assigns it to a
        Pixbuf. Pushes the pixbuf.
        Returns a pixbuf that can be assigned to a layer.
        """
        line_color_alpha = int("0x{0}ff".format(
            self.line_color[1:]), base=16)
        pixbuf_color = GdkPixbuf.Pixbuf.new(
            GdkPixbuf.Colorspace.RGB, True, 8, 16, 16)
        pixbuf_color.fill(line_color_alpha)
        return pixbuf_color

    def get_rgba(self):
        """
        Returns the RGBA for lines (great and small circles) of the
        current layer.
        __!!__ does not return alpha yet
        """
        rgba = Gdk.RGBA()
        rgba.parse(self.line_color)
        return rgba.to_color()

    def get_marker_rgba(self):
        """
        Returns the marker RGBA of the current layer.
        __!!__ does not return alpha yet
        """
        rgba = Gdk.RGBA()
        rgba.parse(self.marker_fill)
        return rgba.to_color()

    def get_pole_rgba(self):
        """
        Returns the pole RGBA of the current layer.
        __!!__ does not return alpha yet
        """
        rgba = Gdk.RGBA()
        rgba.parse(self.pole_fill)
        return rgba.to_color()

    def get_pole_edge_rgba(self):
        """
        Returns the pole edge RGBA of the current layer.
        __!!__ does not return alpha yet
        """
        rgba = Gdk.RGBA()
        rgba.parse(self.pole_edge_color)
        return rgba.to_color()

    def get_marker_edge_rgba(self):
        """
        Returns the marker edge RGBA of the current layer.
        __!!__ does not return alpha yet
        """
        rgba = Gdk.RGBA()
        rgba.parse(self.marker_edge_color)
        return rgba.to_color()

    def get_data_treestore(self):
        """
        Returns the data treestore associated with this layer.
        """
        return self.data_treestore

    def get_data_treeview(self):
        """
        Returns the data treeview associated with this layer.
        """
        return self.data_treeview
     
    def get_layer_type(self):
        """
        Returns the layer type of this object.
        """
        return self.type

    def get_line_color(self):
        """
        Returns the line color set for this layer.
        """
        return self.line_color

    def set_line_color(self, new_color):
        """
        Sets a new line color for this layer.
        """
        self.line_color = new_color

    def get_label(self):
        """
        Returns the label assigned to this layer.
        """
        return self.label

    def set_label(self, new_label):
        """
        Sets a new label for the layer.
        """
        self.label = new_label

    def get_line_width(self):
        """
        Returns the line width that is set for this layer.
        """
        return self.line_width

    def set_line_width(self, new_line_width):
        """
        Assigns a new line width to this layer.
        """
        self.line_width = new_line_width

    def get_line_style(self):
        """
        Returns the line style assigned to this layer.
        """
        return self.line_style

    def set_line_style(self, new_line_style):
        """
        Sets a new line style for this layer.
        """
        self.line_style = new_line_style

    def get_capstyle(self):
        """
        Returns the capstyle that is used in this layer.
        """
        return self.capstyle

    def set_capstyle(self, new_capstyle):
        """
        Sets a new capstyle for this layer.
        """
        self.capstyle = new_capstyle

    def get_pole_style(self):
        """
        Returns the pole style of this layer.
        """
        return self.pole_style

    def set_pole_style(self, new_pole_style):
        """
        Sets a new pole style for this layer.
        """
        self.pole_style = new_pole_style

    def get_pole_size(self):
        """
        Returns the pole size of this layer.
        """
        return self.pole_size

    def set_pole_size(self, new_pole_size):
        """
        Sets a new pole size for this layer.
        """
        self.pole_size = new_pole_size

    def get_pole_fill(self):
        """
        Returns the pole fill of this layer.
        """
        return self.pole_fill

    def set_pole_fill(self, new_pole_fill):
        """
        Sets a new pole fill for this layer.
        """
        self.pole_fill = new_pole_fill

    def get_pole_edge_color(self):
        """
        Return the pole edge color of this layer.
        """
        return self.pole_edge_color

    def set_pole_edge_color(self, new_pole_edge_color):
        """
        Sets a new pole edge color for this layer.
        """
        self.pole_edge_color = new_pole_edge_color

    def get_pole_edge_width(self):
        """
        Returns the pole edge width of this layer.
        """
        return self.pole_edge_width

    def set_pole_edge_width(self, new_pole_edge_width):
        """
        Sets a new pole edge width of this layer.
        """
        self.pole_edge_width = new_pole_edge_width

    def get_pole_alpha(self):
        """
        Returns the transparency of the pole of this layer.
        """
        return self.pole_alpha

    def get_marker_style(self):
        """
        Returns the marker style set for this layer.
        """
        return self.marker_style

    def set_marker_style(self, new_marker_style):
        """
        Assigns a new marker style to this layer.
        """
        self.marker_style = new_marker_style

    def get_marker_size(self):
        """
        Returns the marker size of this layer.
        """
        return self.marker_size

    def set_marker_size(self, new_marker_size):
        """
        Sets a new maker size for this layer.
        """
        self.marker_size = new_marker_size

    def get_marker_fill(self):
        """
        Returns the fill color of the makers of this layer.
        """
        return self.marker_fill

    def set_marker_fill(self, new_marker_fill):
        """
        Sets a new fill color for the markers in this layer.
        """
        self.marker_fill = new_marker_fill

    def get_marker_edge_width(self):
        """
        Returns the width of the marker edges of this layer.
        """
        return self.marker_edge_width

    def set_marker_edge_width(self, new_marker_edge_width):
        """
        Sets a new edge width for the markers in this layer.
        """
        self.marker_edge_width = new_marker_edge_width

    def get_marker_edge_color(self):
        """
        Returns the color of the marker edges in this layer.
        """
        return self.marker_edge_color

    def set_marker_edge_color(self, new_marker_edge_color):
        """
        Sets a new edge color for the markers in this layer.
        """
        self.marker_edge_color = new_marker_edge_color

    def get_line_alpha(self):
        """
        Returns the transparency of the lines of this layer.
        """
        return self.line_alpha

    def set_line_alpha(self, new_line_alpha):
        """
        Sets a new transparency for the lines of this layer.
        """
        self.line_alpha = new_line_alpha

    def get_marker_alpha(self):
        """
        Returns the transparency of the markers of this layer.
        """
        return self.marker_alpha

    def set_marker_alpha(self, new_marker_alpha):
        """
        Sets a new transparency for the markers of this layer.
        """
        self.marker_alpha = new_marker_alpha

    def get_render_gcircles(self):
        """
        Returns if great circles should be rendered for this layer.
        """
        return self.render_gcircles

    def set_render_gcircles(self, new_render_gcircles_state):
        """
        Sets if great circles should be drawn for this layer.
        """
        self.render_gcircles = new_render_gcircles_state

    def get_render_poles(self):
        """
        Returns if poles should be rendered for this layer.
        """
        return self.render_poles

    def set_render_poles(self, new_render_poles_state):
        """
        Sets if poles should be rendered for this layer.
        """
        self.render_poles = new_render_poles_state

    def get_render_linears(self):
        """
        Returns if linears should be rendered for this layer.
        """
        return self.render_linears

    def set_render_linears(self, new_render_linears_state):
        """
        Sets if linears should be rendered for this layer.
        """
        self.render_linears = new_render_linears_state

    def get_draw_contour_fills(self):
        """
        Returns if contour fills should be drawn for this layer.
        Returns a boolean. Default is False.
        """
        return self.draw_contour_fills

    def set_draw_contour_fills(self, new_state):
        """
        Sets a new state for wheter contour fills should be drawn for
        this layer. Expects a boolean.
        """
        self.draw_contour_fills = new_state

    def get_draw_contour_lines(self):
        """
        Returns if contour-lines should be drawn for this layer.
        Returns a boolean. Default is False.
        """
        return self.draw_contour_lines

    def set_draw_contour_lines(self, new_state):
        """
        Sets a new state for wheter contour-lines should be drawn for
        this layer. Expects a boolean.
        """
        self.draw_contour_lines = new_state

    def get_draw_contour_labels(self):
        """
        Returns if contour labels should be drawn for this layer.
        Returns a boolean. Default is False.
        """
        return self.draw_contour_labels

    def set_draw_contour_labels(self, new_state):
        """
        Sets a new state for wheter contour labels should be drawn for
        this layer. Expects a boolean.
        """
        self.draw_contour_labels = new_state

    def get_render_pole_contours(self):
        """
        Returns if contours should be drawn for the poles of this layer.
        """
        return self.render_plane_contours

    def set_render_pole_contours(self, new_state):
        """
        Sets a new state for wheter the pole contours should be drawn.
        """
        self.render_plane_contours = new_state

    def get_render_line_contours(self):
        """
        Returns if contours should be drawn for the linears of this layer.
        """
        return self.render_line_contours

    def set_render_line_contours(self, new_state):
        """
        Sets a new state for wheter the line contours should be drawn.
        """
        self.render_line_contours = new_state

    def get_rose_spacing(self):
        """
        Returns the current rose diagram spacing for this layer.
        """
        return self.rose_spacing

    def set_rose_spacing(self, new_spacing):
        """
        Sets a new spacing for the rose diagram for this layer.
        """
        self.rose_spacing = new_spacing

    def get_rose_bottom(self):
        """
        Returns the current rose diagram bottom cutoff for this layer.
        """
        return self.rose_bottom

    def set_rose_bottom(self, new_bottom):
        """
        Sets a new spacing for the rose bottom cutoff for this layer.
        """
        self.rose_bottom = new_bottom

    def get_colormap(self):
        """
        Returns the colormap for contours as a string (e.g. "Blues")
        """
        return self.colormap

    def set_colormap(self, new_colormap):
        """
        Sets a new colormap. Expects a string (e.g. Blues")
        """
        self.colormap = new_colormap

    def get_contour_resolution(self):
        """
        Returns the contour resolution of the layer as an integer (default
        is 100)
        """
        return self.contour_resolution

    def set_contour_resolution(self, new_resolution):
        """
        Sets a new contour resolution. Expects an integer.
        """
        self.contour_resolution = new_resolution

    def get_contour_method(self):
        """
        Returns the contour method of the layer as a string (default:
        "exponential_kamb")
        """
        return self.contour_method

    def set_contour_method(self, new_method):
        """
        Sets a new contour method. Expects an string.
        """
        self.contour_method = new_method

    def get_contour_line_width(self):
        """
        Returns the contour line width as a int or float. Default is 1.
        """
        return self.contour_line_width

    def set_contour_line_width(self, new_width):
        """
        Sets a new contour-line line-width for the current layer. Expects an
        int or float.
        """
        self.contour_line_width = new_width

    def get_contour_line_color(self):
        """
        Returns the color for contour lines (default is "#000000").
        """
        return self.contour_line_color

    def set_contour_line_color(self, new_color):
        """
        Sets a new line colour for contour intervals. Expects a hex triplet
        in the form of e.g. "#ab00ab"
        """
        self.contour_line_color = new_color

    def get_contour_line_rgba(self):
        """
        Returns the contour line RGBA for the current layer. Default is
        "#000000".
        __!!__ does not return alpha yet
        """
        rgba = Gdk.RGBA()
        rgba.parse(self.contour_line_color)
        return rgba.to_color()

    def get_contour_sigma(self):
        """
        Return the sigma value for contour intervalls of this layer as
        an int or float. Default is 3.
        """
        return self.contour_sigma

    def set_contour_sigma(self, new_sigma):
        """
        Sets a new sigma for the contour intervalls of this layer. Expects
        an int or float.
        """
        self.contour_sigma = new_sigma

    def get_contour_line_style(self):
        """
        Returns the line style for contour lines as a string. Default is a solid
        line as "-".
        """
        return self.contour_line_style

    def set_contour_line_style(self, new_style):
        """
        Sets a new line style for the contour-lines of this layer. Expects
        a string (Example "--")
        """
        self.contour_line_style = new_style

    def get_contour_label_size(self):
        """
        Returns the contour label size of the current layer as a int or float.
        Defeault is 12.
        """
        return self.contour_label_size

    def set_contour_label_size(self, new_size):
        """
        Sets a new label size for the contours of this layer. Expects an int or
        float.
        """
        self.contour_label_size = new_size

    def get_use_line_color(self):
        """
        Returns if a color should be used instead of the colormap for
        contour lines as a boolean. Default is True.
        True = Use color, False = Use colormap
        """
        return self.contour_use_line_color

    def set_use_line_color(self, new_state):
        """
        Sets a state for wheter a color should be used instead of a colormap
        for the contour lines. Expects a boolean.
        True = Use color, False = Use colormap
        """
        self.contour_use_line_color = new_state

class FaultPlaneLayer(PlaneLayer):

    """
    The FaulPlaneLayer-class overrides the type and label settings.

    This class sets the type to "faultplane" and the label to "Faulplane layer".
    All other settings and methods are inherited from the PlaneLayer-class.
    """

    def __init__(self, treestore, treeview):
        """
        Initializes the FaulPlaneLayer-class. Sets the type and label.

        The type is set to "faulplane" and the label is set to "Faulplane
        layer". Requires a treestore and treeview to initialize.
        """
        PlaneLayer.__init__(self, treestore, treeview)
        self.type = "faultplane"
        self.label = "Faultplane layer"

class LineLayer(PlaneLayer):

    """
    The LineLayer class inherits from PlaneLayer but changes the type and label

    The LineLayer class only changes the layer-type to "line" and the label to
    "Linear layer". For initialization it needs a treestore and treeview which
    are passed to the PlaneLayer class. The class also overrides the get_pixbuf
    method, because the colored square from the layer-view should reflect the
    fill of the marker.   
    """

    def __init__(self, treestore, treeview):
        """
        Initializes the LineLayer class with type = "line" and a label.

        The initialization requires a treestore and treeview that hold the
        data of the layer. They are passed to the PlaneLayer class. The
        layer-type is set to line and the label to "Linear layer".
        """
        PlaneLayer.__init__(self, treestore, treeview)
        self.type = "line"
        self.label = "Linear layer"

    def get_pixbuf(self):
        """
        This returns the pixbuf-color to be used for the squares in layer-view.

        This method overrides the method in the PlaneLayer class. It returns
        the color of the marker-fill instead of the line-color. This ensures,
        that the colored squares reflect the color of the symbols in the
        stereonet.
        """
        marker_color_alpha = int("0x{0}ff".format(
            self.marker_fill[1:]), base=16)
        pixbuf_color = GdkPixbuf.Pixbuf.new(
            GdkPixbuf.Colorspace.RGB, True, 8, 16, 16)
        pixbuf_color.fill(marker_color_alpha)
        return pixbuf_color

class SmallCircleLayer(PlaneLayer):

    """
    The SmallCircleLayer-class is used for small-circle datasets.

    It sets the type to "smallcircle" and the default label to "Small circle
    layer". All other methods and settings are inherited from the PlaneLayer-
    class.
    """

    def __init__(self, treestore, treeview):
        """
        Initializes the SmallCircleLayer-class.

        Expects a TreeStore and TreeView that are passed to the PlaneLayer-
        class. The layer type is set to "smallcircle" and the label is set
        to "Small cirlce layer".
        """
        PlaneLayer.__init__(self, treestore, treeview)
        self.type = "smallcircle"
        self.label = "Small circle layer"
