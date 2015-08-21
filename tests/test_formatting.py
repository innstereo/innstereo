#!/usr/bin/python3

import pytest
import innstereo
from .json_strings import *


gui = innstereo.startup(testing=True)

def reset_project():
    """
    Deletes all layers.
    """
    selection = gui.layer_view.get_selection()
    selection.select_all()
    gui.on_toolbutton_delete_layer_clicked(widget=None)

def test_plane_drawing_true():
    """
    Asserts the json-string of an emtpy plane layer.
    """
    reset_project()
    store, lyr_obj_new = gui.on_toolbutton_create_plane_dataset_clicked(widget=None)
    selection = gui.layer_view.get_selection()
    selection.select_path(0)
    props = gui.on_toolbutton_layer_properties_clicked(toolbutton=None, testing=True)
    props.on_switch_render_gcircles_state_set(checkbutton=None, state=True)
    props.on_button_layerproperties_apply_clicked(widget=None)
    data = gui.copy_layer()
    assert data == empty_plane_layer_drawing_on

def test_plane_drawing_false():
    """
    Asserts the json-string of a plane layer with great circle drawing off.
    """
    reset_project()
    store, lyr_obj_new = gui.on_toolbutton_create_plane_dataset_clicked(widget=None)
    selection = gui.layer_view.get_selection()
    selection.select_path(0)
    props = gui.on_toolbutton_layer_properties_clicked(toolbutton=None, testing=True)
    props.on_switch_render_gcircles_state_set(checkbutton=None, state=False)
    props.on_button_layerproperties_apply_clicked(widget=None)
    data = gui.copy_layer()
    assert data == empty_plane_layer_drawing_off
