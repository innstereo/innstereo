#!/usr/bin/python3

import pytest
import innstereo

gui = innstereo.startup(testing=True)

def test_create_plane_layer():
    """
    Creates a layer. Asserts whether number of rows is 1.
    """
    gui.on_toolbutton_create_plane_dataset_clicked(widget=None)
    num_rows = 0
    for row in gui.layer_store:
        num_rows += 1
    assert num_rows == 1

def test_delete_layer():
    """
    Deletes the layer from the previous test. Asserts whether number of
    rows is 0.
    """
    selection = gui.layer_view.get_selection()
    selection.select_all()
    gui.on_toolbutton_delete_layer_clicked(widget=None)
    num_rows = 0
    for row in gui.layer_store:
        num_rows += 1
    assert num_rows == 0

def test_rename_layer():
    """
    Creates a layer and then renames it. Asserts whether the layer has the
    new label.
    """
    new_lbl = "New Label"
    gui.on_toolbutton_create_plane_dataset_clicked(widget=None)
    gui.layer_name_edited(widget=None, path="0", new_label=new_lbl)
    lbl = gui.layer_store[0][3].get_label()
    assert lbl == new_lbl
    selection = gui.layer_view.get_selection()
    selection.select_all()
    gui.on_toolbutton_delete_layer_clicked(widget=None)

def test_create_line_layer():
    """
    Creates a linear layer.
    """
    gui.on_toolbutton_create_line_dataset_clicked(widget=None)

def test_create_faultplane_layer():
    """
    Creates a faultplane layer.
    """
    gui.on_toolbutton_create_faultplane_dataset_clicked(widget=None)

def test_create_smallcircle_layer():
    """
    Creates a smallcircle layer.
    """
    gui.on_toolbutton_create_small_circle_clicked(widget=None)

def test_create_group_layer_no_selection():
    """
    Creates a group layer without a selection.
    """
    selection = gui.layer_view.get_selection()
    selection.unselect_all()
    gui.on_toolbutton_create_group_layer_clicked(widget=None)

def test_create_group_layer_with_selectin():
    """
    Creates a group layer with a selection.
    """
    selection = gui.layer_view.get_selection()
    selection.select_all()
    gui.on_toolbutton_create_group_layer_clicked(widget=None)

def test_toggle_drawing_features():
    """
    Toggles feature drawing on and asserts whether the boolean is True.
    """
    gui.on_toolbutton_draw_features_toggled(widget=None)
    assert gui.draw_features == True

def test_add_planar_feature():
    """
    Creates a planar layer and adds an empty row to it.
    """
    selection = gui.layer_view.get_selection()
    selection.select_all()
    gui.on_toolbutton_delete_layer_clicked(widget=None)
    store, lyr_obj_new = gui.on_toolbutton_create_plane_dataset_clicked(widget=None)
    selection.select_path(0)
    gui.on_toolbutton_add_feature_clicked(widget=None)

def test_add_linear_feature():
    """
    Creates a linear layer and adds an empty row to it.
    """
    selection = gui.layer_view.get_selection()
    selection.select_all()
    gui.on_toolbutton_delete_layer_clicked(widget=None)
    store, lyr_obj_new = gui.on_toolbutton_create_line_dataset_clicked(widget=None)
    selection.select_path(0)
    gui.on_toolbutton_add_feature_clicked(widget=None)

def test_add_faultplane_feature():
    """
    Creates a faultplane layer and adds an empty row to it.
    """
    selection = gui.layer_view.get_selection()
    selection.select_all()
    gui.on_toolbutton_delete_layer_clicked(widget=None)
    store, lyr_obj_new = gui.on_toolbutton_create_faultplane_dataset_clicked(widget=None)
    selection.select_path(0)
    gui.on_toolbutton_add_feature_clicked(widget=None)

def test_add_smallcircle_feature():
    """
    Creates a smallcircle layer and adds an empty row to it.
    """
    selection = gui.layer_view.get_selection()
    selection.select_all()
    gui.on_toolbutton_delete_layer_clicked(widget=None)
    store, lyr_obj_new = gui.on_toolbutton_create_small_circle_clicked(widget=None)
    selection.select_path(0)
    gui.on_toolbutton_add_feature_clicked(widget=None)
