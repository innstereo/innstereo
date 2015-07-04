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

        self.props = {"type": "plane",
                      "label": "Plane layer",
                      "page": 0,
                      #Great circle / Small circle properties
                      "draw_gcircles": True,
                      "line_color": "#0000ff",
                      "line_width": 1.0,
                      "line_style": "-",
                      "line_alpha": 1.0,
                      "capstyle": "butt",
                      #Pole properties
                      "draw_poles": False,
                      "pole_style": "^",
                      "pole_size": 8.0,
                      "pole_fill": "#1abd00",
                      "pole_edge_color": "#000000",
                      "pole_edge_width": 1.0,
                      "pole_alpha": 1.0,
                      #Linear properties
                      "draw_linears": True,
                      "marker_style": "o",
                      "marker_size": 8.0,
                      "marker_fill": "#ff7a00",
                      "marker_edge_color": "#000000",
                      "marker_edge_width": 1.0,
                      "marker_alpha": 1.0,
                      #Linear statistics
                      "draw_mean_vector": False,
                      "draw_fisher_sc": False,
                      "fisher_conf": 95,
                      #Rose diagram properties
                      "rose_spacing": 10,
                      "rose_bottom": 0,
                      #Faultplane properties
                      "draw_hoeppener": False,
                      "draw_lp_plane": False,
                      #Contours
                      "draw_contour_fills": False,
                      "draw_contour_lines": False,
                      "draw_contour_labels": False,
                      "colormap": "Blues",
                      "contour_resolution": 40,
                      "contour_method": "exponential_kamb",
                      "contour_sigma": 2,
                      "contour_line_color": "#000000",
                      "contour_use_line_color": True,
                      "contour_line_width": 1,
                      "contour_line_style": "-",
                      "contour_label_size": 12,
                      "manual_range": False,
                      "lower_limit": 1,
                      "upper_limit": 10,
                      "steps": 10
                      }

    def get_page(self):
        """
        Returns the current page

        The current page of the layer-properties dialog is stored
        for each layer. The integer value corresponds to the
        value of the Gtk Notebook.
        """
        return self.props["page"]

    def set_page(self, new_page):
        """
        Sets a new page. Saves the current notebook page.

        Expects an integer that corresponds to the Gtk-Notebook page,
        that was last viewed for this layer.
        """
        self.props["page"] = new_page

    def get_pixbuf(self):
        """
        Returns a pixbuf with the current line-color.

        This method takes the current line-color hex-triplet and adds two
        characters for the transparency (Currently no transparency = ff). Then
        it created a Gdk.Pixbuf, fills it with the color and returns it. This
        method is called by the main window to create the colored squares for
        the layer view.
        """
        line_color_alpha = int("0x{0}ff".format(self.props["line_color"][1:]),
                               base=16)
        pixbuf_color = GdkPixbuf.Pixbuf.new(GdkPixbuf.Colorspace.RGB,
                                            True, 8, 16, 16)
        pixbuf_color.fill(line_color_alpha)
        return pixbuf_color

    def get_rgba(self):
        """
        Returns the RGBA for lines (great or small circles) of the layer.

        This method returns the Gdk.RGBA representation of the current line
        color. This is the color set for great circles in plane and faultplane
        datasets and the color of the small circles in small circle datasets.
        This method is called by the layer properties dialog to set the color
        of the ColorButton for line-color.
        __!!__ Does not return alpha yet!
        """
        rgba = Gdk.RGBA()
        rgba.parse(self.props["line_color"])
        return rgba.to_color()

    def get_marker_rgba(self):
        """
        Returns the RGBA for linear markers of the layer.

        This method returns the Gdk.RGBA representation of the markers of this
        layer. This is the color set for linear elements in line-layers and
        faultplane-layers.
        This method is called by the layer properties dialog to set the color
        of the ColorButton for linear markers.
        __!!__ Does not return alpha yet!
        """
        rgba = Gdk.RGBA()
        rgba.parse(self.props["marker_fill"])
        return rgba.to_color()

    def get_pole_rgba(self):
        """
        Returns the RGBA for pole markers of the layer.

        This method returns the Gdk.RGBA representation of the poles of this
        layer. This is the color set for poles in plane-layers and
        faultplane-layers.
        This method is called by the layer properties dialog to set the color
        of the ColorButton for poles.
        __!!__ Does not return alpha yet!
        """
        rgba = Gdk.RGBA()
        rgba.parse(self.props["pole_fill"])
        return rgba.to_color()

    def get_pole_edge_rgba(self):
        """
        Returns the RGBA for pole edges of the layer.

        This method returns the Gdk.RGBA representation of the edge-color of
        the poles of this layer.
        This method is called by the layer properties dialog to set the color
        of the ColorButton for pole edges.
        __!!__ Does not return alpha yet!
        """
        rgba = Gdk.RGBA()
        rgba.parse(self.props["pole_edge_color"])
        return rgba.to_color()

    def get_marker_edge_rgba(self):
        """
        Returns the RGBA for marker edges of the layer.

        This method returns the Gdk.RGBA representation of the marker-edge-
        color of this layer.
        This method is called by the layer properties dialog to set the color
        of the ColorButton for marker edges.
        __!!__ Does not return alpha yet!
        """
        rgba = Gdk.RGBA()
        rgba.parse(self.props["marker_edge_color"])
        return rgba.to_color()

    def get_data_treestore(self):
        """
        Returns the data TreeStore that holds the data for this layer.

        This method returns the TreeStore that stores the data of this layer.
        The TreeStore contains all the individual features as rows.
        """
        return self.data_treestore

    def get_data_treeview(self):
        """
        Returns the data TreeView that is associated with this layer.

        Each layer stores a TreeView that is linked to the layers' TreeStore.
        This method is called when the selection in the main windows' layer
        view is changed.
        """
        return self.data_treeview

    def get_layer_type(self):
        """
        Returns the layer type of this object.

        The layer type is a string. Either "plane", "faultplane", "line", or
        "smallcircle".
        """
        return self.props["type"]

    def get_line_color(self):
        """
        Returns the line color set for this layer.

        The line color is returned as a hex-triplet. It is the color of
        great circles for planes and faultplanes and the color of the small
        circles.
        """
        return self.props["line_color"]

    def set_line_color(self, new_color):
        """
        Sets a new line color for this layer.

        Expects a string in hex-triplet format.
        """
        self.props["line_color"] = new_color

    def get_label(self):
        """
        Returns the label assigned to this layer.

        The label is returned as a string. After a new layer is created this
        is a default hardcoded value. The user can change this string.
        """
        return self.props["label"]

    def set_label(self, new_label):
        """
        Sets a new label for the layer.

        Expects a string. This method is called when the user changes the
        name of a layer by editing the column in the layer-view.
        """
        self.props["label"] = new_label

    def get_line_width(self):
        """
        Returns the line width that is set for this layer.

        The line width is returned as int or float. It is the width or weight
        of the great circles or small circles.
        """
        return self.props["line_width"]

    def set_line_width(self, new_line_width):
        """
        Assigns a new line width to this layer.

        Expects a int or float. This method is called by the layer-properties
        dialog when a new value has been set.
        """
        self.props["line_width"] = new_line_width

    def get_line_style(self):
        """
        Returns the line style assigned to this layer.

        Returns the line value as a string. The default is a solid line
        (which corresponds to "-").
        """
        return self.props["line_style"]

    def set_line_style(self, new_line_style):
        """
        Sets a new line style for this layer.

        Expects a string (e.g. "-" for a solid line). This method is called
        by the layer properties dialog when a new value for this has been
        set.
        """
        self.props["line_style"] = new_line_style

    def get_capstyle(self):
        """
        Returns the line capstyle that is used in this layer.

        The line capstyle is returned as a string. The default is "butt" and
        is only used when the line is dashed or dash-dotted.
        """
        return self.props["capstyle"]

    def set_capstyle(self, new_capstyle):
        """
        Sets a new capstyle for this layer.

        Expects a string (e.g. "round").
        """
        self.props["capstyle"] = new_capstyle

    def get_pole_style(self):
        """
        Returns the pole style of this layer.

        The style of the marker used for poles is returned as a string. The
        default is "o".
        """
        return self.props["pole_style"]

    def set_pole_style(self, new_pole_style):
        """
        Sets a new pole style for this layer.

        Expects a string. This method is called by the layer-properties dialog
        when a new style is set.
        """
        self.props["pole_style"] = new_pole_style

    def get_pole_size(self):
        """
        Returns the pole size of this layer.

        The pole size is returned as int or float.
        """
        return self.props["pole_size"]

    def set_pole_size(self, new_pole_size):
        """
        Sets a new pole size for this layer.

        Expects an int or float. This method is called by layer-properties
        dialog when a new value is set.
        """
        self.props["pole_size"] = new_pole_size

    def get_pole_fill(self):
        """
        Returns the pole fill color of this layer.

        The fill of the pole markers is returned as a hex-triplet.
        """
        return self.props["pole_fill"]

    def set_pole_fill(self, new_pole_fill):
        """
        Sets a new pole fill for this layer.

        Expects a string in hex-triplet format. This method is called by the
        layer-properties dialog when a new color is set.
        """
        self.props["pole_fill"] = new_pole_fill

    def get_pole_edge_color(self):
        """
        Return the pole edge color of this layer.

        The pole edge color is returned as a hex-triplet.
        """
        return self.props["pole_edge_color"]

    def set_pole_edge_color(self, new_pole_edge_color):
        """
        Sets a new pole edge color for this layer.

        Expects a string in hex-triplet format. This method is called by
        the layer-properties dialog when a new edge color is set.
        """
        self.props["pole_edge_color"] = new_pole_edge_color

    def get_pole_edge_width(self):
        """
        Returns the pole edge width of this layer.

        The pole edge width is returned as an int or float.
        """
        return self.props["pole_edge_width"]

    def set_pole_edge_width(self, new_pole_edge_width):
        """
        Sets a new pole edge width of this layer.

        Expects an int or float. This method is called by the layer-properties
        dialog when a new value is set.
        """
        self.props["pole_edge_width"] = new_pole_edge_width

    def get_pole_alpha(self):
        """
        Returns the transparency of the pole of this layer.

        The transparency is returned as a float between 0 and 1.
        """
        return self.props["pole_alpha"]

    def set_pole_alpha(self, new_alpha):
        """
        Sets a new transparency for the pole markers.

        Expects a float value between 0 and 1.
        """
        self.props["pole_alpha"] = new_alpha

    def get_marker_style(self):
        """
        Returns the marker style set for this layer.

        The marker style is returned as a string symbol. The default value
        is "o". This method is called by the main windoweach time the plot is
        redrawn.
        """
        return self.props["marker_style"]

    def set_marker_style(self, new_marker_style):
        """
        Assigns a new marker style to this layer.

        Expects a string. This method is called by the layer-properties dialog
        when a new value is set for this layer.
        """
        self.props["marker_style"] = new_marker_style

    def get_marker_size(self):
        """
        Returns the marker size of this layer.

        The marker size is returned as an int or float. This method is called
        by the main window each time the plot is redrawn.
        """
        return self.props["marker_size"]

    def set_marker_size(self, new_marker_size):
        """
        Sets a new maker size for this layer.

        Expects an int or float. This method is called by the layer-properties
        dialog when a new value is set.
        """
        self.props["marker_size"] = new_marker_size

    def get_marker_fill(self):
        """
        Returns the fill color of the makers for linear elments of this layer.

        The fill color is returned as a string in hex-triplet format. This
        method is called by the redraw_plot-method of the MainWindow and the
        layer-properties dialog.
        """
        return self.props["marker_fill"]

    def set_marker_fill(self, new_marker_fill):
        """
        Sets a new fill color for the markers in this layer.

        Expects a string in hex-triplet format. This method is called by the
        layer-properties dialog when a new value is set.
        """
        self.props["marker_fill"] = new_marker_fill

    def get_marker_edge_width(self):
        """
        Returns the width of the marker edges of this layer.

        The width is returned as int or float. This method is called by
        the redraw_plot-method of the MainWindow-class and the layer-properties
        dialog.
        """
        return self.props["marker_edge_width"]

    def set_marker_edge_width(self, new_marker_edge_width):
        """
        Sets a new edge width for the markers in this layer.

        Expects an int or float. This method is called by the layer-properties
        dialog when a new value is set.
        """
        self.props["marker_edge_width"] = new_marker_edge_width

    def get_marker_edge_color(self):
        """
        Returns the color of the marker edges in this layer.

        The color is returned as a string in hex-triplet format. This method
        is called by the redraw_plot-method of the MainWindow-class and the
        layer-properties dialog.
        """
        return self.props["marker_edge_color"]

    def set_marker_edge_color(self, new_marker_edge_color):
        """
        Sets a new edge color for the markers in this layer.

        Expects a string in hex-triplet format. This method is called
        by the layer-properties dialog when a new value is set.
        """
        self.props["marker_edge_color"] = new_marker_edge_color

    def get_line_alpha(self):
        """
        Returns the transparency of the lines of this layer.

        The transparency is returned as a float between 0 and 1.
        """
        return self.props["line_alpha"]

    def set_line_alpha(self, new_line_alpha):
        """
        Sets a new transparency for the lines of this layer.

        Expects a float between 0 and 1. This method is called by the
        layer-properties dialog when a new value is set.
        """
        self.props["line_alpha"] = new_line_alpha

    def get_marker_alpha(self):
        """
        Returns the transparency of the markers of this layer.

        The transparency is returned as a float between 0 and 1.
        """
        return self.props["marker_alpha"]

    def set_marker_alpha(self, new_marker_alpha):
        """
        Sets a new transparency for the markers of this layer.

        Expects a float between 0 and 1. This method is called by the
        layer-properties dialog when a new value has been set.
        """
        self.props["marker_alpha"] = new_marker_alpha

    def get_draw_gcircles(self):
        """
        Returns if great circles should be rendered for this layer.

        The returned value is a bool. True mean that circles are rendered.
        False mean they are not rendered.
        """
        return self.props["draw_gcircles"]

    def set_draw_gcircles(self, new_draw_gcircles_state):
        """
        Sets if great circles should be drawn for this layer.

        Expects a boolean. This method is called by the layer-properties
        dialog when a new value is set.
        """
        self.pros["draw_gcircles"] = new_draw_gcircles_state

    def get_draw_poles(self):
        """
        Returns if poles should be rendered for this layer.

        The returned value is a boolean. True means that poles are rendered.
        False means that they are not rendered.
        """
        return self.props["draw_poles"]

    def set_draw_poles(self, new_draw_poles_state):
        """
        Sets if poles should be rendered for this layer.

        Expects a boolean. This method is called by the layer-properties
        dialog when a new value is set.
        """
        self.props["draw_poles"] = new_draw_poles_state

    def get_draw_linears(self):
        """
        Returns if linears should be rendered for this layer.

        Returns a boolean. True means that linears are drawn. False means
        that they are not drawn.
        """
        return self.props["draw_linears"]

    def set_draw_linears(self, new_draw_linears_state):
        """
        Sets if linears should be rendered for this layer.

        Expects a boolean. This method is called by the layer-properties
        dialog when a new value is set.
        """
        self.props["draw_linears"] = new_draw_linears_state

    def get_draw_contour_fills(self):
        """
        Returns if contour fills should be drawn for this layer.

        Returns a boolean. Default is False. True mean that contour fills are
        drawn. False means they are not drawn.
        """
        return self.props["draw_contour_fills"]

    def set_draw_contour_fills(self, new_state):
        """
        Sets a new state for whether contour fills are drawn for this layer.

        Expects a boolean. This method is called by the layer-properties
        dialog when a new value is set.
        """
        self.props["draw_contour_fills"] = new_state

    def get_draw_contour_lines(self):
        """
        Returns if contour-lines should be drawn for this layer.

        Returns a boolean. Default is False. True means that contour-lines
        are drawn. False mean they are not drawn.
        """
        return self.props["draw_contour_lines"]

    def set_draw_contour_lines(self, new_state):
        """
        Sets if contour-lines should be drawn for this layer.

        Expects a boolean. This method is called by the layer-properties
        dialog when a new value is set.
        """
        self.props["draw_contour_lines"] = new_state

    def get_draw_contour_labels(self):
        """
        Returns if contour labels should be drawn for this layer.

        Returns a boolean. Default is False. True mean that contour labels
        are drawn. False means they are not drawn.
        """
        return self.props["draw_contour_labels"]

    def set_draw_contour_labels(self, new_state):
        """
        Sets if labels should be drawn for this layer.

        Expects a boolean. This method is called by the layer-properties
        dialog when a new value is set.
        """
        self.props["draw_contour_labels"] = new_state

    def get_rose_spacing(self):
        """
        Returns the current rose diagram spacing for this layer.

        The returned value is an int or float.
        """
        return self.props["rose_spacing"]

    def set_rose_spacing(self, new_spacing):
        """
        Sets a new spacing for the rose diagram for this layer.

        Expects an int or float. This method is called by the layer-properties
        dialog when a new value is set.
        """
        self.props["rose_spacing"] = new_spacing

    def get_rose_bottom(self):
        """
        Returns the current rose diagram bottom cutoff for this layer.

        The returned value is an int of float.
        """
        return self.props["rose_bottom"]

    def set_rose_bottom(self, new_bottom):
        """
        Sets a new spacing for the rose bottom cutoff for this layer.

        Expects an int or float. This method is called by the layer-properties
        dialog when a new value is set.        
        """
        self.props["rose_bottom"] = new_bottom

    def get_colormap(self):
        """
        Returns the colormap for contours as a string.

        Default is "Blues".
        """
        return self.props["colormap"]

    def set_colormap(self, new_colormap):
        """
        Sets a new colormap.

        Expects a string (e.g. "Blues")
        """
        self.props["colormap"] = new_colormap

    def get_contour_resolution(self):
        """
        Returns the contour resolution of the layer as an integer.

        Default is 100.
        """
        return self.props["contour_resolution"]

    def set_contour_resolution(self, new_resolution):
        """
        Sets a new contour resolution.

        Expects an integer.
        """
        self.props["contour_resolution"] = new_resolution

    def get_contour_method(self):
        """
        Returns the contour method of the layer as a string.

        Default: "exponential_kamb"
        """
        return self.props["contour_method"]

    def set_contour_method(self, new_method):
        """
        Sets a new contour method.

        Expects an string.
        """
        self.props["contour_method"] = new_method

    def get_contour_line_width(self):
        """
        Returns the contour line width as a int or float.

        Default is 1.
        """
        return self.props["contour_line_width"]

    def set_contour_line_width(self, new_width):
        """
        Sets a new contour-line line-width for the current layer.

        Expects an int or float.
        """
        self.props["contour_line_width"] = new_width

    def get_contour_line_color(self):
        """
        Returns the color for contour lines.

        Default is "#000000".
        """
        return self.props["contour_line_color"]

    def set_contour_line_color(self, new_color):
        """
        Sets a new line colour for contour intervals.

        Expects a hex triplet in the form of e.g. "#ab00ab".
        """
        self.props["contour_line_color"] = new_color

    def get_contour_line_rgba(self):
        """
        Returns the contour line RGBA for the current layer.

        Default is "#000000".
        __!!__ does not return alpha yet
        """
        rgba = Gdk.RGBA()
        rgba.parse(self.props["contour_line_color"])
        return rgba.to_color()

    def get_contour_sigma(self):
        """
        Return the sigma value for contour intervalls of this layer.

        Returned value can be int or float. The default is 3.
        """
        return self.props["contour_sigma"]

    def set_contour_sigma(self, new_sigma):
        """
        Sets a new sigma for the contour intervalls of this layer.

        Expects an int or float.
        """
        self.props["contour_sigma"] = new_sigma

    def get_contour_line_style(self):
        """
        Returns the line style for contour lines as a string.

        Default is a solid line as "-".
        """
        return self.props["contour_line_style"]

    def set_contour_line_style(self, new_style):
        """
        Sets a new line style for the contour-lines of this layer.

        Expects a string (Example "--").
        """
        self.props["contour_line_style"] = new_style

    def get_contour_label_size(self):
        """
        Returns the contour label size of the current layer.

        This method expects an int or float. The default is 12.
        """
        return self.props["contour_label_size"]

    def set_contour_label_size(self, new_size):
        """
        Sets a new label size for the contours of this layer.

        This method expects an int or float.
        """
        self.props["contour_label_size"] = new_size

    def get_use_line_color(self):
        """
        Returns whether a color or colormap is used for contour lines.

        Returns if a color should be used instead of the colormap for
        contour lines as a boolean. Default is True.
        True = Use color, False = Use colormap
        """
        return self.props["contour_use_line_color"]

    def set_use_line_color(self, new_state):
        """
        Sets whether a color or colormap is used for contour lines.

        Sets a state for whether a color should be used instead of a colormap
        for the contour lines. Expects a boolean.
        True = Use color, False = Use colormap
        """
        self.props["contour_use_line_color"] = new_state

    def get_draw_hoeppener(self):
        """
        Returns if Hoeppener Arrows should be drawn.

        Function is called by the MainWindow by the redraw_plot function to
        check if the arrows should be drawn. It is also called by the
        LayerProperties-dialog to update the interface to the current settings.
        """
        return self.props["draw_hoeppener"]

    def set_draw_hoeppener(self, new_state):
        """
        Sets whether the Hoeppener arrows should be drawn.

        Function is called by the layer-properties dialog when a new state
        is set. The function expects a boolean.
        """
        self.props["draw_hoeppener"] = new_state

    def get_draw_lp_plane(self):
        """
        Returns if the Linear-Pole-plane should be drawn.

        Function is called by the MainWindow by the redraw_plot function to
        check if the linear-pole-plane should be drawn.
        """
        return self.props["draw_lp_plane"]

    def set_draw_lp_plane(self, new_state):
        """
        Sets whether the Linear-Pole-plane should be drawn.

        Function is called by the layer-properties dialog when a new state
        is set. The function expects a boolean.
        """
        self.props["draw_lp_plane"] = new_state

    def get_manual_range(self):
        """
        Returns if the a manual range should be used for contouring.

        Called from the LayerProperties class to set the state of the switch
        and from the MainWindow class to determine the drawing of contours.
        Returns a boolean. Default is False.
        """
        return self.props["manual_range"]

    def set_manual_range(self, new_state):
        """
        Sets whether a manual range should be used to draw contours.

        Expects a boolean. Called from the LayerProperties class when a new
        state is set for the button.
        """
        self.props["manual_range"] = new_state

    def get_lower_limit(self):
        """
        """
        return self.props["lower_limit"]

    def set_lower_limit(self, new_lower):
        """
        """
        self.props["lower_limit"] = new_lower

    def get_upper_limit(self):
        """
        """
        return self.props["upper_limit"]

    def set_upper_limit(self, new_upper):
        """
        """
        self.props["upper_limit"] = new_upper

    def get_steps(self):
        """
        """
        return self.props["steps"]

    def set_steps(self, new_steps):
        """
        """
        self.props["steps"] = new_steps

    def return_data(self):
        """
        Returns the data in stored for this layer as a list.

        Iterates over the treestore associated with this layer and copies all
        data into a list of rows. Returns the list.
        """
        store_data = []
        def iterate_over_data(model, path, itr):
            row = model[path]
            store_data.append([row[0], row[1], row[2]])

        self.data_treestore.foreach(iterate_over_data)
        return store_data

    def get_properties(self):
        """
        Returns a dictionary containing all the properties of the layer.

        The returned dictionary contains all colors, labels, etc. set by the
        user. This method is used for saving layers, or passing a layer to
        the copy-paste-function or the drag-and-drop function.
        """
        return self.props.copy()

    def set_properties(self, props):
        """
        Sets all layer properties to the values of the passed dictionary.

        Expects a dictionary of all layer properties (excluding the layer
        type, which is set during creation of the layer). This method is
        called when a project is loaded or when a layer is pasted, or
        received through drag-and-drop.
        """
        self.props = props

    def get_draw_mean_vector(self):
        """
        Returns if the mean vector should be drawn.
        """
        return self.props["draw_mean_vector"]

    def set_draw_mean_vector(self, new_state):
        """
        Sets a new state whether the mean direction linar should be drawn.
        """
        self.props["draw_mean_vector"] = new_state

    def get_draw_fisher_sc(self):
        """
        Returns if the confidence small circle should be drawn.
        """
        return self.props["draw_fisher_sc"]

    def set_draw_fisher_sc(self, new_state):
        """
        Sets a new state whether the confidence small circle should be drawn.
        """
        self.props["draw_fisher_sc"] = new_state

    def get_fisher_conf(self):
        """
        Returns the confidence for calculating the Fisher Statistics.
        """
        return self.props["fisher_conf"]

    def set_fisher_conf(self, new_conf):
        """
        Sets a new confidene for calculating the Fisher Statistics.
        """
        self.props["fisher_conf"] = new_conf


class FaultPlaneLayer(PlaneLayer):

    """
    The FaultPlaneLayer-class overrides the type and label settings.

    This class sets the type to "faultplane" and the label to
    "Faultplane layer". All other settings and methods are inherited from
    the PlaneLayer-class.
    """

    def __init__(self, treestore, treeview):
        """
        Initializes the FaultPlaneLayer-class. Sets the type and label.

        The type is set to "faultplane" and the label is set to "Faultplane
        layer". Requires a treestore and treeview to initialize.
        """
        PlaneLayer.__init__(self, treestore, treeview)
        self.props["type"] = "faultplane"
        self.props["label"] = "Faultplane layer"


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
        self.props["type"] = "line"
        self.props["label"] = "Linear layer"
        self.props["page"] = 1

    def get_pixbuf(self):
        """
        This returns the pixbuf-color to be used for the squares in layer-view.

        This method overrides the method in the PlaneLayer class. It returns
        the color of the marker-fill instead of the line-color. This ensures,
        that the colored squares reflect the color of the symbols in the
        stereonet.
        """
        marker_color_alpha = int("0x{0}ff".format(
            self.props["marker_fill"][1:]), base=16)
        pixbuf_color = GdkPixbuf.Pixbuf.new(
            GdkPixbuf.Colorspace.RGB, True, 8, 16, 16)
        pixbuf_color.fill(marker_color_alpha)
        return pixbuf_color


class EigenVectorLayer(PlaneLayer):

    """
    This class is used for the results of eigenvector calculations

    It inherits from the PlaneLayer class and defines a new type and label.
    On init it expects a treestore and treeview that are passed to the
    PlaneLayer class.
    """

    def __init__(self, treestore, treeview):
        """
        Initializes the EigenVectorLayer class.

        Expects a treestore and treeview that are passed to the PlaneLayer
        class. Overrides the self.type and self.label of the PlaneLayer class.
        """
        PlaneLayer.__init__(self, treestore, treeview)
        self.props["type"] = "eigenvector"
        self.props["label"] = "Eigenvector layer"
        self.props["page"] = 1

    def get_pixbuf(self):
        """
        Returns the pixbuf for eigenvectors, which is based on the marker fill.

        Evaluates the marker fill, creates GdkPixbuf with that color and
        returns it.
        """
        marker_color_alpha = int("0x{0}ff".format(
            self.props["marker_fill"][1:]), base=16)
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
        to "Small circle layer".
        """
        PlaneLayer.__init__(self, treestore, treeview)
        self.props["type"] = "smallcircle"
        self.props["label"] = "Small circle layer"
        
