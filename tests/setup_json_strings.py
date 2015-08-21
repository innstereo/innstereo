#!/usr/bin/python3

"""
This module sets up the jsong-strings for the tests.

This needs to be run after defaults are changed so that the comparisons
work again. To set up the json file use:

$   python3 -m tests
"""

import os

def reset_project(gui):
    """
    Deletes all layers.
    """
    selection = gui.layer_view.get_selection()
    selection.select_all()
    gui.on_toolbutton_delete_layer_clicked(widget=None)

def gather_data(gui):
    """
    Creates layers and features and appends their JSON dumps to a list.
    """
    strings = []

    var = "empty_plane_layer_drawing_on"
    reset_project(gui)
    store, lyr_obj_new = gui.on_toolbutton_create_plane_dataset_clicked(widget=None)
    selection = gui.layer_view.get_selection()
    selection.select_path(0)
    data = gui.copy_layer()
    strings.append([var, data])

    var = "empty_plane_layer_drawing_off"
    reset_project(gui)
    store, lyr_obj_new = gui.on_toolbutton_create_plane_dataset_clicked(widget=None)
    selection = gui.layer_view.get_selection()
    selection.select_path(0)
    props = gui.on_toolbutton_layer_properties_clicked(toolbutton=None, testing=True)
    props.on_switch_render_gcircles_state_set(checkbutton=None, state=False)
    props.on_button_layerproperties_apply_clicked(widget=None)
    data = gui.copy_layer()
    strings.append([var, data])

    return strings

def write_data(strings):
    """
    Writes the list of variable-names and json-strings to a file.
    """
    with open("tests/json_strings.py", "w", newline="") as js:
        for string in strings:
            js.write("{} = '''{}'''\n".format(string[0], string[1]))

def run(gui):
    strings = gather_data(gui)
    write_data(strings)    
