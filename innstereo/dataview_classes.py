#!/usr/bin/python3

"""
Controls the appearance and behaviour of the liststores shown in the data-view.

This module contains classes that control the appearance and behaviour of
the ListStores that are shown in the lower left side of the GUI. The
DataTreeView-class inherits from Gtk.TreeView and is a superclass of all other
classes in this module. The other classes are PlaneDataView, FaultPlaneDataView,
LineDataView, and SmallCircleDataView.
Sources:
on_key_pressed:
http://stackoverflow.com/questions/15497766/python-pygoobject-treeview-
confirm-edit-after-move-between-cells-with-tab-key
"""

from gi.repository import Gtk, Gdk, GLib


class DataTreeView(Gtk.TreeView):

    """
    This class inherits from Gtk.TreeView. It requires a treestore and the
    main window redraw-function for the init. The class defines a function
    that truncates the float-numbers and a function to tab through the
    treeview. All other data-views inherit from this class.
    """

    def __init__(self, store, redraw_plot):
        """
        Initializes the treeview. Requires a model and the main window
        redraw-function. Sets selection mode to MULTIPLE. Connect the
        key-press event.
        """
        Gtk.TreeView.__init__(self, model=store)
        self.store = store
        self.redraw = redraw_plot
        self.select = self.get_selection()
        self.select.set_mode(Gtk.SelectionMode.MULTIPLE)
        self.connect("key-press-event", self.on_key_pressed)

    def truncate(self, number):
        """
        Rounds and truncates a number to one decimal place. Used for all
        float numbers in the data-view. The numbers are preserved with
        full float precision.
        """
        number = round(number, 1)
        return number

    def on_key_pressed(self, treeview, event):
        """
        Triggered when a key is pressed while the TreeView is active.
        If the Tab key was pressed the current value in the active cell
        is saved and the cursor jumps to the next cell and makes it editable.
        """
        keyname = Gdk.keyval_name(event.keyval)
        path, col = treeview.get_cursor()
        columns = [c for c in treeview.get_columns() if c.get_visible()]
        colnum = columns.index(col)

        if keyname == "Tab" or keyname == "Esc":
            if colnum + 1 < len(columns):
                next_column = columns[colnum + 1]
            else:
                tmodel = treeview.get_model()
                titer = tmodel.iter_next(tmodel.get_iter(path))
                if titer is None:
                    titer = tmodel.get_iter_first()
                path = tmodel.get_path(titer)
                next_column = columns[0]

            if keyname == "Tab":
                GLib.timeout_add(50,
                                 treeview.set_cursor,
                                 path, next_column, True)
            elif keyname == "Escape":
                pass

class PlaneDataView(DataTreeView):

    """
    This class is used for planes. The View consists of dip-direction, dip,
    and stratigraphic orientation.
    """

    def __init__(self, store, redraw_plot):
        """
        Passes store and redraw_plot to the parent DataTreeView-class.
        Initializes 3 columns and connects their edited-signals. The columns:
        0: Dip direction (Float)
        1: Dip angle (Float)
        2: Stratigraphy (String)
        """
        DataTreeView.__init__(self, store, redraw_plot)

        renderer_dir = Gtk.CellRendererText()
        renderer_dir.set_property("editable", True)
        column_dir = Gtk.TreeViewColumn("Dir", renderer_dir, text=0)
        column_dir.set_alignment(0.5)
        column_dir.set_expand(True)
        column_dir.set_cell_data_func(renderer_dir, 
                    lambda col, cell, model, iter, unused:
                    cell.set_property("text",
                    "{0}".format(self.truncate(model.get(iter, 0)[0]))))
        self.append_column(column_dir)

        renderer_dip = Gtk.CellRendererText()
        renderer_dip.set_property("editable", True)
        column_dip = Gtk.TreeViewColumn("Dip", renderer_dip, text=1)
        column_dip.set_alignment(0.5)
        column_dip.set_expand(True)
        column_dip.set_cell_data_func(renderer_dip, 
                    lambda col, cell, model, iter, unused:
                    cell.set_property("text",
                    "{0}".format(self.truncate(model.get(iter, 1)[0]))))
        self.append_column(column_dip)

        renderer_strat = Gtk.CellRendererText()
        renderer_strat.set_property("editable", True)
        column_strat = Gtk.TreeViewColumn("Strat", renderer_strat, text=2)
        column_strat.set_alignment(0.5)
        column_strat.set_expand(True)
        self.append_column(column_strat)

        renderer_dir.connect("edited", self.renderer_dir_edited)
        renderer_dip.connect("edited", self.renderer_dip_edited)
        renderer_strat.connect("edited", self.renderer_strat_edited)

    def renderer_dir_edited(self, widget, path, new_string):
        """
        If the dip direction is edited, replace the existing value.
        The function replaces a ","- with a "."-comma. Converts
        the string value to a float.
        """
        self.store[path][0] = float(new_string.replace(",", "."))
        self.redraw()

    def renderer_dip_edited(self, widget, path, new_string):
        """
        If the dip angle is edited, replace the existing value.
        The function replaces a ","- with a "."-comma. Converts
        the string value to a float.
        """
        self.store[path][1] = float(new_string.replace(",", "."))
        self.redraw()

    def renderer_strat_edited(self, widget, path, new_string):
        """
        If the stratigraphic orientation direction is edited, replace the
        existing value. The column takes the raw string.
        """
        self.store[path][2] = new_string
        self.redraw()

class FaultPlaneDataView(DataTreeView):

    """
    This class is used for faultplanes. It inherits the truncate
    and tab-through function from the DataTreeView class.
    """

    def __init__(self, store, redraw_plot):
        """
        Initializes a new faultplane view. 5 columns are created and their
        respective edited-signals are connected. The columns are:
        0: Plane dip direction (Float)
        1: Plane dip (Float)
        2: Lineation dip direction (Float)
        3: Lineation dip (Float)
        4: Lineation sense of movement (String)
        """
        DataTreeView.__init__(self, store, redraw_plot)

        renderer_dir = Gtk.CellRendererText()
        renderer_dir.set_property("editable", True)
        column_dir = Gtk.TreeViewColumn("Dir", renderer_dir, text=0)
        column_dir.set_alignment(0.5)
        column_dir.set_expand(True)
        column_dir.set_cell_data_func(renderer_dir, 
                    lambda col, cell, model, iter, unused:
                    cell.set_property("text",
                    "{0}".format(self.truncate(model.get(iter, 0)[0]))))
        self.append_column(column_dir)

        renderer_dip = Gtk.CellRendererText()
        renderer_dip.set_property("editable", True)
        column_dip = Gtk.TreeViewColumn("Dip", renderer_dip, text=1)
        column_dip.set_alignment(0.5)
        column_dip.set_expand(True)
        column_dip.set_cell_data_func(renderer_dip, 
                    lambda col, cell, model, iter, unused:
                    cell.set_property("text",
                    "{0}".format(self.truncate(model.get(iter, 1)[0]))))
        self.append_column(column_dip)

        renderer_ldir = Gtk.CellRendererText()
        renderer_ldir.set_property("editable", True)
        column_ldir = Gtk.TreeViewColumn("L-Dir", renderer_ldir, text=2)
        column_ldir.set_alignment(0.5)
        column_ldir.set_expand(True)
        column_ldir.set_cell_data_func(renderer_ldir, 
                    lambda col, cell, model, iter, unused:
                    cell.set_property("text",
                    "{0}".format(self.truncate(model.get(iter, 2)[0]))))
        self.append_column(column_ldir)

        renderer_ldip = Gtk.CellRendererText()
        renderer_ldip.set_property("editable", True)
        column_ldip = Gtk.TreeViewColumn("L-Dip", renderer_ldip, text=3)
        column_ldip.set_alignment(0.5)
        column_ldip.set_expand(True)
        column_ldip.set_cell_data_func(renderer_ldip, 
                    lambda col, cell, model, iter, unused:
                    cell.set_property("text",
                    "{0}".format(self.truncate(model.get(iter, 3)[0]))))
        self.append_column(column_ldip)

        renderer_sense = Gtk.CellRendererText()
        renderer_sense.set_property("editable", True)
        column_sense = Gtk.TreeViewColumn("Sense", renderer_sense, text=4)
        column_sense.set_alignment(0.5)
        column_sense.set_expand(True)
        self.append_column(column_sense)

        renderer_dir.connect("edited", self.renderer_dir_edited)
        renderer_dip.connect("edited", self.renderer_dip_edited)
        renderer_ldir.connect("edited", self.renderer_ldir_edited)
        renderer_ldip.connect("edited", self.renderer_ldip_edited)
        renderer_sense.connect("edited", self.renderer_sense_edited)

    def renderer_dir_edited(self, widget, path, new_string):
        """
        If the dip direction is edited, replace the existing value.
        The function replaces a ","- with a "."-comma. Converts
        the string value to a float.
        """
        self.store[path][0] = float(new_string.replace(",", "."))
        self.redraw()

    def renderer_dip_edited(self, widget, path, new_string):
        """
        If the dip angle is edited, replace the existing value.
        The function replaces a ","- with a "."-comma. Converts
        the string value to a float.
        """
        self.store[path][1] = float(new_string.replace(",", "."))
        self.redraw()

    def renderer_ldir_edited(self, widget, path, new_string):
        """
        If the linear dip direction is edited, replace the existing value.
        The function replaces a ","- with a "."-comma. Converts
        the string value to a float.
        """
        self.store[path][2] = float(new_string.replace(",", "."))
        self.redraw()

    def renderer_ldip_edited(self, widget, path, new_string):
        """
        If the linear dip is edited, replace the existing value.
        The function replaces a ","- with a "."-comma. Converts
        the string value to a float.
        """
        self.store[path][3] = float(new_string.replace(",", "."))
        self.redraw()

    def renderer_sense_edited(self, widget, path, new_string):
        """
        If the linear shear sense is edited, replace the existing value.
        The the values is replaced by the raw input-string.
        """
        self.store[path][4] = new_string
        self.redraw()

class LineDataView(DataTreeView):

    """
    This class is used for linear data. It inherits the truncate
    and tab-through function from the DataTreeView class. It creates 3 columns
    for dip direction, dip and linear direction sense.
    """

    def __init__(self, store, redraw_plot):
        """
        Initalizes the LineDataView class. Passes 2 arguments to the
        DataTreeView class and creates 3 TreeViewColumns and connects their
        edited-signals. The columns are:
        0: Dip direction (Float)
        1: Dip (Float)
        2: Sense of direction/movement (String)
        """
        DataTreeView.__init__(self, store, redraw_plot)

        renderer_dir = Gtk.CellRendererText()
        renderer_dir.set_property("editable", True)
        column_dir = Gtk.TreeViewColumn("Dir", renderer_dir, text=0)
        column_dir.set_alignment(0.5)
        column_dir.set_expand(True)
        column_dir.set_cell_data_func(renderer_dir, 
                    lambda col, cell, model, iter, unused:
                    cell.set_property("text",
                    "{0}".format(self.truncate(model.get(iter, 0)[0]))))
        self.append_column(column_dir)
        
        renderer_dip = Gtk.CellRendererText()
        renderer_dip.set_property("editable", True)
        column_dip = Gtk.TreeViewColumn("Dip", renderer_dip, text=1)
        column_dip.set_alignment(0.5)
        column_dip.set_expand(True)
        column_dip.set_cell_data_func(renderer_dip, 
                    lambda col, cell, model, iter, unused:
                    cell.set_property("text",
                    "{0}".format(self.truncate(model.get(iter, 1)[0]))))
        self.append_column(column_dip)

        renderer_sense = Gtk.CellRendererText()
        renderer_sense.set_property("editable", True)
        column_sense = Gtk.TreeViewColumn("Sense", renderer_sense, text=2)
        column_sense.set_alignment(0.5)
        column_sense.set_expand(True)
        self.append_column(column_sense)

        renderer_dir.connect("edited", self.renderer_dir_edited)
        renderer_dip.connect("edited", self.renderer_dip_edited)
        renderer_sense.connect("edited", self.renderer_sense_edited)

    def renderer_dir_edited(self, widget, path, new_string):
        """
        If the dip direction is edited, replace the existing value.
        The function replaces a ","- with a "."-comma. Converts
        the string value to a float.
        """
        self.store[path][0] = float(new_string.replace(",", "."))
        self.redraw()

    def renderer_dip_edited(self, widget, path, new_string):
        """
        If the dip angle is edited, replace the existing value.
        The function replaces a ","- with a "."-comma. Converts
        the string value to a float.
        """
        self.store[path][1] = float(new_string.replace(",", "."))
        self.redraw()

    def renderer_sense_edited(self, widget, path, new_string):
        """
        If the sense of the linear is edited, replace the existing value.
        The new values is the raw input-string.
        """
        self.store[path][2] = new_string
        self.redraw()

class SmallCircleDataView(DataTreeView):

    """
    This class is used for small circle datasets. It inherits from DataTreeView.
    It creates 3 columns for dip direction, dip and opening angle.
    """

    def __init__(self, store, redraw_plot):
        """
        Initalizes the SmallCircleDataView class. Passes 2 arguments to the
        DataTreeView class and creates 3 TreeViewColumns and connects their
        edited-signals. The columns are:
        0: Dip direction (Float)
        1: Dip (Float)
        2: Opening angle (Float)
        """
        DataTreeView.__init__(self, store, redraw_plot)

        renderer_dir = Gtk.CellRendererText()
        renderer_dir.set_property("editable", True)
        column_dir = Gtk.TreeViewColumn("Dir", renderer_dir, text=0)
        column_dir.set_alignment(0.5)
        column_dir.set_expand(True)
        column_dir.set_cell_data_func(renderer_dir, 
                    lambda col, cell, model, iter, unused:
                    cell.set_property("text",
                    "{0}".format(self.truncate(model.get(iter, 0)[0]))))
        self.append_column(column_dir)
        
        renderer_dip = Gtk.CellRendererText()
        renderer_dip.set_property("editable", True)
        column_dip = Gtk.TreeViewColumn("Dip", renderer_dip, text=1)
        column_dip.set_alignment(0.5)
        column_dip.set_expand(True)
        column_dip.set_cell_data_func(renderer_dip, 
                    lambda col, cell, model, iter, unused:
                    cell.set_property("text",
                    "{0}".format(self.truncate(model.get(iter, 1)[0]))))
        self.append_column(column_dip)

        renderer_angle = Gtk.CellRendererText()
        renderer_angle.set_property("editable", True)
        column_angle = Gtk.TreeViewColumn("Angle", renderer_angle, text=2)
        column_angle.set_alignment(0.5)
        column_angle.set_expand(True)
        column_angle.set_cell_data_func(renderer_angle, 
                    lambda col, cell, model, iter, unused:
                    cell.set_property("text",
                    "{0}".format(self.truncate(model.get(iter, 2)[0]))))
        self.append_column(column_angle)

        renderer_dir.connect("edited", self.renderer_dir_edited)
        renderer_dip.connect("edited", self.renderer_dip_edited)
        renderer_angle.connect("edited", self.renderer_angle_edited)

    def renderer_dir_edited(self, widget, path, new_string):
        """
        If the dip direction is edited, replace the existing value.
        The function replaces a ","- with a "."-comma. Converts
        the string value to a float.
        """
        self.store[path][0] = float(new_string.replace(",", "."))
        self.redraw()

    def renderer_dip_edited(self, widget, path, new_string):
        """
        If the dip is edited, replace the existing value.
        The function replaces a ","- with a "."-comma. Converts
        the string value to a float.
        """
        self.store[path][1] = float(new_string.replace(",", "."))
        self.redraw()

    def renderer_angle_edited(self, widget, path, new_string):
        """
        If the opening angle is edited, replace the existing value.
        The function replaces a ","- with a "."-comma. Converts
        the string value to a float.
        """
        self.store[path][2] = float(new_string.replace(",", "."))
        self.redraw()


class EigenVectorView(DataTreeView):

    """
    The EigenVectorView is used for EigenVectorLayer-class layers.

    This class creates 3 columsn for the dip-direction and dip of the
    eigenvector and the eigenvalues. The class inherits from the DataTreeView
    class.
    """

    def __init__(self, store, redraw_plot):
        """
        Sets up 3 columns and connects their signals.

        On init, the treestore-object and redraw_plto function are passed to
        the DataTreeView class. 3 columns are set up and their signals for
        being edited are connected.
        """
        DataTreeView.__init__(self, store, redraw_plot)

        renderer_dir = Gtk.CellRendererText()
        renderer_dir.set_property("editable", True)
        column_dir = Gtk.TreeViewColumn("Dir", renderer_dir, text=0)
        column_dir.set_alignment(0.5)
        column_dir.set_expand(True)
        column_dir.set_cell_data_func(renderer_dir, 
                    lambda col, cell, model, iter, unused:
                    cell.set_property("text",
                    "{0}".format(self.truncate(model.get(iter, 0)[0]))))
        self.append_column(column_dir)
        
        renderer_dip = Gtk.CellRendererText()
        renderer_dip.set_property("editable", True)
        column_dip = Gtk.TreeViewColumn("Dip", renderer_dip, text=1)
        column_dip.set_alignment(0.5)
        column_dip.set_expand(True)
        column_dip.set_cell_data_func(renderer_dip, 
                    lambda col, cell, model, iter, unused:
                    cell.set_property("text",
                    "{0}".format(self.truncate(model.get(iter, 1)[0]))))
        self.append_column(column_dip)

        renderer_value = Gtk.CellRendererText()
        renderer_value.set_property("editable", True)
        column_value = Gtk.TreeViewColumn("Eigenvalue", renderer_value, text=2)
        column_value.set_alignment(0.5)
        column_value.set_expand(True)
        column_value.set_cell_data_func(renderer_value, 
                    lambda col, cell, model, iter, unused:
                    cell.set_property("text",
                    "{0}".format(self.truncate(model.get(iter, 2)[0]))))
        self.append_column(column_value)

        renderer_dir.connect("edited", self.renderer_dir_edited)
        renderer_dip.connect("edited", self.renderer_dip_edited)
        renderer_value.connect("edited", self.renderer_value_edited)

    def renderer_dir_edited(self, widget, path, new_string):
        """
        If the dip direction is edited, replace the existing value.
        The function replaces a ","- with a "."-comma. Converts
        the string value to a float.
        """
        self.store[path][0] = float(new_string.replace(",", "."))
        self.redraw()

    def renderer_dip_edited(self, widget, path, new_string):
        """
        If the dip angle is edited, replace the existing value.
        The function replaces a ","- with a "."-comma. Converts
        the string value to a float.
        """
        self.store[path][1] = float(new_string.replace(",", "."))
        self.redraw()

    def renderer_value_edited(self, widget, path, new_string):
        """
        Triggered when the value is edited.

        The new value is converted to a float and commas are replaced by
        dots. Then the new value is assigned to the cell.
        """
        self.store[path][2] = float(new_string.replace(",", "."))
        self.redraw()
