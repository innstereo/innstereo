#!/usr/bin/python3

"""
Controls the behaviour of the treeview for the layer-view.

This module contains the LayerTreeView class. It controls the behaviour and
appearance of the layer-view which is in the upper left side of the GUI. The
class inherits from Gtk.TreeView and requires a Gtk.TreeStore to initialize.
"""

from gi.repository import Gtk, Gdk


class LayerTreeView(Gtk.TreeView):

    """
    Controls the behaviour of the treeview for the layer-view.

    This class controls the behaviour and appearance of the layer-view
    which is in the upper left side of the GUI. The class inherits from
    Gtk.TreeView and requires a Gtk.TreeStore to initialize.
    """

    def __init__(self, store):
        """
        Initializes the TreeViewColumns and some special behaviour.

        Removes the headers, enables the tree-lines, turns the selection-mode
        to multiple. Adds a column for the toggle, the pixbuf and the name
        of the layer.
        """
        Gtk.TreeView.__init__(self, store)
        self.store = store
        self.set_headers_visible(False)
        self.set_enable_tree_lines(True)
        self.select = self.get_selection()
        self.select.set_mode(Gtk.SelectionMode.MULTIPLE)
        self.set_property("can-focus", True)

        targets = [("text/plain", 0, 0)]
        self.enable_model_drag_source(Gdk.ModifierType.BUTTON1_MASK,
                                      targets,
                                      Gdk.DragAction.MOVE)
        self.enable_model_drag_dest(targets, Gdk.DragAction.MOVE)

        self.renderer_activate_layer = Gtk.CellRendererToggle()
        self.column_activate_layer = Gtk.TreeViewColumn("",
                                                   self.renderer_activate_layer,
                                                   active=0)
        self.append_column(self.column_activate_layer)

        icon_renderer = Gtk.CellRendererPixbuf()
        icon_column = Gtk.TreeViewColumn("", icon_renderer, pixbuf=1)
        self.append_column(icon_column)

        self.renderer_name = Gtk.CellRendererText(weight=700,
                                                  weight_set=True)
        self.column_name = Gtk.TreeViewColumn("Layer",
                                              self.renderer_name, text=2)
        self.column_name.set_min_width(100)
        self.renderer_name.set_property("editable", True)
        self.column_name.set_resizable(True)
        self.append_column(self.column_name)
