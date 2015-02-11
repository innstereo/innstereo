#!/usr/bin/python3

from gi.repository import Gtk, Gdk

class LayerTreeView(Gtk.TreeView):
    def __init__(self, store):
        Gtk.TreeView.__init__(self, store)
        self.store = store
        self.set_headers_visible(False)
        self.set_enable_tree_lines(True)
        self.select = self.get_selection()
        self.select.set_mode(Gtk.SelectionMode.MULTIPLE)
        self.set_property("can-focus", True)

        #targets = [("text/uri-list", 0, 0)]
        #self.enable_model_drag_source(Gdk.ModifierType.BUTTON1_MASK,
        #    targets, Gdk.DragAction.DEFAULT|Gdk.DragAction.MOVE)
        #self.enable_model_drag_dest(targets, Gdk.DragAction.DEFAULT)

        self.renderer_activate_layer = Gtk.CellRendererToggle()
        self.column_activate_layer = Gtk.TreeViewColumn("",
            self.renderer_activate_layer, active=0)
        self.append_column(self.column_activate_layer)

        icon_renderer = Gtk.CellRendererPixbuf()
        icon_column = Gtk.TreeViewColumn("", icon_renderer, pixbuf=1)
        self.append_column(icon_column)

        self.renderer_name = Gtk.CellRendererText(weight=700, weight_set=True)
        self.column_name = Gtk.TreeViewColumn(
            "Layer", self.renderer_name, text=2)
        self.column_name.set_min_width(100)
        self.renderer_name.set_property("editable", True)
        self.column_name.set_resizable(True)
        self.append_column(self.column_name)
