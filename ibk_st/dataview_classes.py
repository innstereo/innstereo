#!/usr/bin/python3

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
        key-pres event.
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
        Enables going through the treeview-cells by pressing tab.
        Source: http://stackoverflow.com/questions/15497766/python-pygoobject-treeview-confirm-edit-after-move-between-cells-with-tab-key
        """
        keyname = Gdk.keyval_name(event.keyval)
        path, col = treeview.get_cursor() 
        columns = [c for c in treeview.get_columns() if c.get_visible()] 
        colnum = columns.index(col)     

        if keyname=="Tab" or keyname=="Esc":
            if colnum + 1 < len(columns): 
                next_column = columns[colnum + 1]               
            else: 
                tmodel = treeview.get_model() 
                titer = tmodel.iter_next(tmodel.get_iter(path)) 
                if titer is None: 
                    titer = tmodel.get_iter_first() 
                path = tmodel.get_path(titer) 
                next_column = columns[0] 

            if keyname == 'Tab':
                GLib.timeout_add(50,
                                treeview.set_cursor,
                                path, next_column, True)
            elif keyname == 'Escape':
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
        column_dir.set_cell_data_func(renderer_dir, \
                    lambda col, cell, model, iter, unused:
                    cell.set_property("text",
                    "{0}".format(self.truncate(model.get(iter, 0)[0]))))
        self.append_column(column_dir)
        
        renderer_dip = Gtk.CellRendererText()
        renderer_dip.set_property("editable", True)
        column_dip = Gtk.TreeViewColumn("Dip", renderer_dip, text=1)
        column_dip.set_alignment(0.5)
        column_dip.set_expand(True)
        column_dip.set_cell_data_func(renderer_dip, \
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
        """
        self.store[path][0] = float(new_string.replace(',', '.'))
        self.redraw()

    def renderer_dip_edited(self, widget, path, new_string):
        """
        If the dip angle is edited, replace the existing value.
        """
        self.store[path][1] = float(new_string.replace(',', '.'))
        self.redraw()

    def renderer_strat_edited(self, widget, path, new_string):
        """
        If the stratigraphic orientation direction is edited, replace the
        existing value.
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
        column_dir.set_cell_data_func(renderer_dir, \
                    lambda col, cell, model, iter, unused:
                    cell.set_property("text",
                    "{0}".format(self.truncate(model.get(iter, 0)[0]))))
        self.append_column(column_dir)
        
        renderer_dip = Gtk.CellRendererText()
        renderer_dip.set_property("editable", True)
        column_dip = Gtk.TreeViewColumn("Dip", renderer_dip, text=1)
        column_dip.set_alignment(0.5)
        column_dip.set_expand(True)
        column_dip.set_cell_data_func(renderer_dip, \
                    lambda col, cell, model, iter, unused:
                    cell.set_property("text",
                    "{0}".format(self.truncate(model.get(iter, 1)[0]))))
        self.append_column(column_dip)

        renderer_ldir = Gtk.CellRendererText()
        renderer_ldir.set_property("editable", True)
        column_ldir = Gtk.TreeViewColumn("L-Dir", renderer_ldir, text=2)
        column_ldir.set_alignment(0.5)
        column_ldir.set_expand(True)
        column_ldir.set_cell_data_func(renderer_ldir, \
                    lambda col, cell, model, iter, unused:
                    cell.set_property("text",
                    "{0}".format(self.truncate(model.get(iter, 2)[0]))))
        self.append_column(column_ldir)

        renderer_ldip = Gtk.CellRendererText()
        renderer_ldip.set_property("editable", True)
        column_ldip = Gtk.TreeViewColumn("L-Dip", renderer_ldip, text=3)
        column_ldip.set_alignment(0.5)
        column_ldip.set_expand(True)
        column_ldip.set_cell_data_func(renderer_ldip, \
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
        """
        self.store[path][0] = float(new_string.replace(',', '.'))
        self.redraw()

    def renderer_dip_edited(self, widget, path, new_string):
        """
        If the dip angle is edited, replace the existing value.
        """
        self.store[path][1] = float(new_string.replace(',', '.'))
        self.redraw()

    def renderer_ldir_edited(self, widget, path, new_string):
        """
        If the linear dip direction is edited, replace the existing value.
        """
        self.store[path][2] = float(new_string.replace(',', '.'))
        self.redraw()

    def renderer_ldip_edited(self, widget, path, new_string):
        """
        If the linear dip is edited, replace the existing value.
        """
        self.store[path][3] = float(new_string.replace(',', '.'))
        self.redraw()

    def renderer_sense_edited(self, widget, path, new_string):
        """
        If the linear shear sense is edited, replace the existing value.
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
        column_dir.set_cell_data_func(renderer_dir, \
                    lambda col, cell, model, iter, unused:
                    cell.set_property("text",
                    "{0}".format(self.truncate(model.get(iter, 0)[0]))))
        self.append_column(column_dir)
        
        renderer_dip = Gtk.CellRendererText()
        renderer_dip.set_property("editable", True)
        column_dip = Gtk.TreeViewColumn("Dip", renderer_dip, text=1)
        column_dip.set_alignment(0.5)
        column_dip.set_expand(True)
        column_dip.set_cell_data_func(renderer_dip, \
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
        """
        self.store[path][0] = float(new_string.replace(',', '.'))
        self.redraw()

    def renderer_dip_edited(self, widget, path, new_string):
        """
        If the dip angle is edited, replace the existing value.
        """
        self.store[path][1] = float(new_string.replace(',', '.'))
        self.redraw()

    def renderer_sense_edited(self, widget, path, new_string):
        """
        If the sense of the linear is edited, replace the existing value.
        """
        self.store[path][4] = new_string
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
        column_dir.set_cell_data_func(renderer_dir, \
                    lambda col, cell, model, iter, unused:
                    cell.set_property("text",
                    "{0}".format(self.truncate(model.get(iter, 0)[0]))))
        self.append_column(column_dir)
        
        renderer_dip = Gtk.CellRendererText()
        renderer_dip.set_property("editable", True)
        column_dip = Gtk.TreeViewColumn("Dip", renderer_dip, text=1)
        column_dip.set_alignment(0.5)
        column_dip.set_expand(True)
        column_dip.set_cell_data_func(renderer_dip, \
                    lambda col, cell, model, iter, unused:
                    cell.set_property("text",
                    "{0}".format(self.truncate(model.get(iter, 1)[0]))))
        self.append_column(column_dip)

        renderer_angle = Gtk.CellRendererText()
        renderer_angle.set_property("editable", True)
        column_angle = Gtk.TreeViewColumn("Angle", renderer_angle, text=2)
        column_angle.set_alignment(0.5)
        column_angle.set_expand(True)
        column_angle.set_cell_data_func(renderer_angle, \
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
        """
        self.store[path][0] = float(new_string.replace(',', '.'))
        self.redraw()

    def renderer_dip_edited(self, widget, path, new_string):
        """
        If the dip is edited, replace the existing value.
        """
        self.store[path][1] = float(new_string.replace(',', '.'))
        self.redraw()

    def renderer_angle_edited(self, widget, path, new_string):
        """
        If the opening angle is edited, replace the existing value.
        """
        self.store[path][2] = float(new_string.replace(',', '.'))
        self.redraw()
