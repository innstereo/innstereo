#!/usr/bin/python3

import pytest
import innstereo

gui = innstereo.startup(testing=True)

def reset_project():
    """
    Deletes all layers.
    """
    selection = gui.layer_view.get_selection()
    selection.select_all()
    gui.on_toolbutton_delete_layer_clicked(widget=None)

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

def test_create_group_layer_with_selection():
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
    reset_project()
    store, lyr_obj_new = gui.on_toolbutton_create_plane_dataset_clicked(widget=None)
    selection = gui.layer_view.get_selection()
    selection.select_path(0)
    gui.on_toolbutton_add_feature_clicked(widget=None)

def test_add_linear_feature():
    """
    Creates a linear layer and adds an empty row to it.
    """
    reset_project()
    store, lyr_obj_new = gui.on_toolbutton_create_line_dataset_clicked(widget=None)
    selection = gui.layer_view.get_selection()
    selection.select_path(0)
    gui.on_toolbutton_add_feature_clicked(widget=None)

def test_add_faultplane_feature():
    """
    Creates a faultplane layer and adds an empty row to it.
    """
    reset_project()
    store, lyr_obj_new = gui.on_toolbutton_create_faultplane_dataset_clicked(widget=None)
    selection = gui.layer_view.get_selection()
    selection.select_path(0)
    gui.on_toolbutton_add_feature_clicked(widget=None)

def test_add_smallcircle_feature():
    """
    Creates a smallcircle layer and adds an empty row to it.
    """
    reset_project()
    store, lyr_obj_new = gui.on_toolbutton_create_small_circle_clicked(widget=None)
    selection = gui.layer_view.get_selection()
    selection.select_path(0)
    gui.on_toolbutton_add_feature_clicked(widget=None)

def test_copy_plane():
    """
    Copies a plane layer with one feature and assert the string.
    """
    plane_copy = """{"filetype": "InnStereo layer 1.0", "layers": [["0", {"arrow_color": "#d51e1e", "capstyle": "butt", "colormap": "viridis", "contour_label_size": 12, "contour_line_color": "#000000", "contour_line_style": "-", "contour_line_width": 1, "contour_method": "exponential_kamb", "contour_resolution": 40, "contour_sigma": 2, "contour_use_line_color": true, "dip_rose_spacing": 10, "draw_angelier": true, "draw_contour_fills": false, "draw_contour_labels": false, "draw_contour_lines": false, "draw_fisher_sc": false, "draw_gcircles": true, "draw_hoeppener": false, "draw_linears": true, "draw_lp_plane": false, "draw_mean_vector": false, "draw_poles": false, "fisher_conf": 95, "label": "Plane Layer", "line_alpha": 1.0, "line_color": "#0000ff", "line_style": "-", "line_width": 1.0, "lower_limit": 1, "manual_range": false, "marker_alpha": 1.0, "marker_edge_color": "#000000", "marker_edge_width": 1.0, "marker_fill": "#ff7a00", "marker_size": 8.0, "marker_style": "o", "page": 0, "pole_alpha": 1.0, "pole_edge_color": "#000000", "pole_edge_width": 1.0, "pole_fill": "#1abd00", "pole_size": 8.0, "pole_style": "^", "rose_bottom": 0, "rose_spacing": 10, "steps": 10, "type": "plane", "upper_limit": 10}, [[120.0, 30.0, ""]]]]}"""
    reset_project()
    store, lyr_obj_new = gui.on_toolbutton_create_plane_dataset_clicked(widget=None)
    selection = gui.layer_view.get_selection()
    selection.select_path(0)
    gui.add_planar_feature(store, 120, 30, "")
    data = gui.on_toolbutton_copy_clicked(toolbutton=None)
    assert data == plane_copy

def test_copy_linear():
    """
    Copies a line layer with one feature and asserts the string.
    """
    line_copy = """{"filetype": "InnStereo layer 1.0", "layers": [["0", {"arrow_color": "#d51e1e", "capstyle": "butt", "colormap": "viridis", "contour_label_size": 12, "contour_line_color": "#000000", "contour_line_style": "-", "contour_line_width": 1, "contour_method": "exponential_kamb", "contour_resolution": 40, "contour_sigma": 2, "contour_use_line_color": true, "dip_rose_spacing": 10, "draw_angelier": true, "draw_contour_fills": false, "draw_contour_labels": false, "draw_contour_lines": false, "draw_fisher_sc": false, "draw_gcircles": true, "draw_hoeppener": false, "draw_linears": true, "draw_lp_plane": false, "draw_mean_vector": false, "draw_poles": false, "fisher_conf": 95, "label": "Linear Layer", "line_alpha": 1.0, "line_color": "#0000ff", "line_style": "-", "line_width": 1.0, "lower_limit": 1, "manual_range": false, "marker_alpha": 1.0, "marker_edge_color": "#000000", "marker_edge_width": 1.0, "marker_fill": "#69b3ff", "marker_size": 8.0, "marker_style": "o", "page": 1, "pole_alpha": 1.0, "pole_edge_color": "#000000", "pole_edge_width": 1.0, "pole_fill": "#1abd00", "pole_size": 8.0, "pole_style": "^", "rose_bottom": 0, "rose_spacing": 10, "steps": 10, "type": "line", "upper_limit": 10}, [[240.0, 60.0, "up"]]]]}"""
    reset_project()
    store, lyr_obj_new = gui.on_toolbutton_create_line_dataset_clicked(widget=None)
    selection = gui.layer_view.get_selection()
    selection.select_path(0)
    gui.add_linear_feature(store, 240, 60, "up")
    data = gui.on_toolbutton_copy_clicked(toolbutton=None)
    assert data == line_copy

def test_copy_faultplane():
    """
    Copies a faultplane layer with one feature and asserts the string.
    """
    faultplane_copy = """{"filetype": "InnStereo layer 1.0", "layers": [["0", {"arrow_color": "#d51e1e", "capstyle": "butt", "colormap": "viridis", "contour_label_size": 12, "contour_line_color": "#000000", "contour_line_style": "-", "contour_line_width": 1, "contour_method": "exponential_kamb", "contour_resolution": 40, "contour_sigma": 2, "contour_use_line_color": true, "dip_rose_spacing": 10, "draw_angelier": true, "draw_contour_fills": false, "draw_contour_labels": false, "draw_contour_lines": false, "draw_fisher_sc": false, "draw_gcircles": true, "draw_hoeppener": false, "draw_linears": true, "draw_lp_plane": false, "draw_mean_vector": false, "draw_poles": false, "fisher_conf": 95, "label": "Faultplane Layer", "line_alpha": 1.0, "line_color": "#000000", "line_style": "-", "line_width": 1.0, "lower_limit": 1, "manual_range": false, "marker_alpha": 1.0, "marker_edge_color": "#000000", "marker_edge_width": 1.0, "marker_fill": "#ffffff", "marker_size": 8.0, "marker_style": "o", "page": 0, "pole_alpha": 1.0, "pole_edge_color": "#000000", "pole_edge_width": 1.0, "pole_fill": "#1abd00", "pole_size": 8.0, "pole_style": "^", "rose_bottom": 0, "rose_spacing": 10, "steps": 10, "type": "faultplane", "upper_limit": 10}, [[45.0, 30.0, 45.0]]]]}"""
    reset_project()
    store, lyr_obj_new = gui.on_toolbutton_create_faultplane_dataset_clicked(widget=None)
    selection = gui.layer_view.get_selection()
    selection.select_path(0)
    gui.add_faultplane_feature(store, 45, 30, 45, 30, "dn")
    data = gui.on_toolbutton_copy_clicked(toolbutton=None)
    assert data == faultplane_copy

def test_copy_smallcircle():
    """
    Copies a smallcircle layer with one feature and asserts the string.
    """
    smallcircle_copy = """{"filetype": "InnStereo layer 1.0", "layers": [["0", {"arrow_color": "#d51e1e", "capstyle": "butt", "colormap": "viridis", "contour_label_size": 12, "contour_line_color": "#000000", "contour_line_style": "-", "contour_line_width": 1, "contour_method": "exponential_kamb", "contour_resolution": 40, "contour_sigma": 2, "contour_use_line_color": true, "dip_rose_spacing": 10, "draw_angelier": true, "draw_contour_fills": false, "draw_contour_labels": false, "draw_contour_lines": false, "draw_fisher_sc": false, "draw_gcircles": true, "draw_hoeppener": false, "draw_linears": true, "draw_lp_plane": false, "draw_mean_vector": false, "draw_poles": false, "fisher_conf": 95, "label": "Small-Circle Layer", "line_alpha": 1.0, "line_color": "#0000ff", "line_style": "-", "line_width": 1.0, "lower_limit": 1, "manual_range": false, "marker_alpha": 1.0, "marker_edge_color": "#000000", "marker_edge_width": 1.0, "marker_fill": "#ff7a00", "marker_size": 8.0, "marker_style": "o", "page": 0, "pole_alpha": 1.0, "pole_edge_color": "#000000", "pole_edge_width": 1.0, "pole_fill": "#1abd00", "pole_size": 8.0, "pole_style": "^", "rose_bottom": 0, "rose_spacing": 10, "steps": 10, "type": "smallcircle", "upper_limit": 10}, [[320.0, 40.0, 25.0]]]]}"""
    reset_project()
    store, lyr_obj_new = gui.on_toolbutton_create_small_circle_clicked(widget=None)
    selection = gui.layer_view.get_selection()
    selection.select_path(0)
    gui.add_smallcircle_feature(store, 320, 40, 25)
    data = gui.on_toolbutton_copy_clicked(toolbutton=None)
    assert data == smallcircle_copy

def test_copy_eigenvector():
    """
    Copies a eigenvector layer with one feature and asserts the string.
    """
    eigenvector_copy = """{"filetype": "InnStereo layer 1.0", "layers": [["0", {"arrow_color": "#d51e1e", "capstyle": "butt", "colormap": "viridis", "contour_label_size": 12, "contour_line_color": "#000000", "contour_line_style": "-", "contour_line_width": 1, "contour_method": "exponential_kamb", "contour_resolution": 40, "contour_sigma": 2, "contour_use_line_color": true, "dip_rose_spacing": 10, "draw_angelier": true, "draw_contour_fills": false, "draw_contour_labels": false, "draw_contour_lines": false, "draw_fisher_sc": false, "draw_gcircles": true, "draw_hoeppener": false, "draw_linears": true, "draw_lp_plane": false, "draw_mean_vector": false, "draw_poles": false, "fisher_conf": 95, "label": "Eigenvector Layer", "line_alpha": 1.0, "line_color": "#0000ff", "line_style": "-", "line_width": 1.0, "lower_limit": 1, "manual_range": false, "marker_alpha": 1.0, "marker_edge_color": "#000000", "marker_edge_width": 1.0, "marker_fill": "#ff7a00", "marker_size": 8.0, "marker_style": "o", "page": 1, "pole_alpha": 1.0, "pole_edge_color": "#000000", "pole_edge_width": 1.0, "pole_fill": "#1abd00", "pole_size": 8.0, "pole_style": "^", "rose_bottom": 0, "rose_spacing": 10, "steps": 10, "type": "eigenvector", "upper_limit": 10}, [[160.0, 80.0, 0.876]]]]}"""
    reset_project()
    store, lyr_obj_new = gui.add_layer_dataset("eigenvector")
    selection = gui.layer_view.get_selection()
    selection.select_path(0)
    gui.add_eigenvector_feature(store, 160, 80, 0.876)
    data = gui.on_toolbutton_copy_clicked(toolbutton=None)
    assert data == eigenvector_copy

def test_copy_group_layer():
    """
    Copies a group layer (folder) and asserts the string.
    """
    folder_copy = """{"filetype": "InnStereo layer 1.0", "layers": [["0", {"label": "Layer Group", "type": "folder"}, []]]}"""
    reset_project()
    gui.on_toolbutton_create_group_layer_clicked(widget=None)
    selection = gui.layer_view.get_selection()
    selection.select_path(0)
    data = gui.on_toolbutton_copy_clicked(toolbutton=None)
    assert data == folder_copy

def test_plane_intersect():
    """
    Creates two plane layers; calculates the intersect; Asserts the project.
    """
    lyr_copy = """{"filetype": "InnStereo data file 1.0", "layers": [["0", {"arrow_color": "#d51e1e", "capstyle": "butt", "colormap": "viridis", "contour_label_size": 12, "contour_line_color": "#000000", "contour_line_style": "-", "contour_line_width": 1, "contour_method": "exponential_kamb", "contour_resolution": 40, "contour_sigma": 2, "contour_use_line_color": true, "dip_rose_spacing": 10, "draw_angelier": true, "draw_contour_fills": false, "draw_contour_labels": false, "draw_contour_lines": false, "draw_fisher_sc": false, "draw_gcircles": true, "draw_hoeppener": false, "draw_linears": true, "draw_lp_plane": false, "draw_mean_vector": false, "draw_poles": false, "fisher_conf": 95, "label": "Plane Layer", "line_alpha": 1.0, "line_color": "#0000ff", "line_style": "-", "line_width": 1.0, "lower_limit": 1, "manual_range": false, "marker_alpha": 1.0, "marker_edge_color": "#000000", "marker_edge_width": 1.0, "marker_fill": "#ff7a00", "marker_size": 8.0, "marker_style": "o", "page": 0, "pole_alpha": 1.0, "pole_edge_color": "#000000", "pole_edge_width": 1.0, "pole_fill": "#1abd00", "pole_size": 8.0, "pole_style": "^", "rose_bottom": 0, "rose_spacing": 10, "steps": 10, "type": "plane", "upper_limit": 10}, [[140.0, 50.0, ""]]], ["1", {"arrow_color": "#d51e1e", "capstyle": "butt", "colormap": "viridis", "contour_label_size": 12, "contour_line_color": "#000000", "contour_line_style": "-", "contour_line_width": 1, "contour_method": "exponential_kamb", "contour_resolution": 40, "contour_sigma": 2, "contour_use_line_color": true, "dip_rose_spacing": 10, "draw_angelier": true, "draw_contour_fills": false, "draw_contour_labels": false, "draw_contour_lines": false, "draw_fisher_sc": false, "draw_gcircles": true, "draw_hoeppener": false, "draw_linears": true, "draw_lp_plane": false, "draw_mean_vector": false, "draw_poles": false, "fisher_conf": 95, "label": "Plane Layer", "line_alpha": 1.0, "line_color": "#0000ff", "line_style": "-", "line_width": 1.0, "lower_limit": 1, "manual_range": false, "marker_alpha": 1.0, "marker_edge_color": "#000000", "marker_edge_width": 1.0, "marker_fill": "#ff7a00", "marker_size": 8.0, "marker_style": "o", "page": 0, "pole_alpha": 1.0, "pole_edge_color": "#000000", "pole_edge_width": 1.0, "pole_fill": "#1abd00", "pole_size": 8.0, "pole_style": "^", "rose_bottom": 0, "rose_spacing": 10, "steps": 10, "type": "plane", "upper_limit": 10}, [[270.0, 60.0, ""]]], ["2", {"arrow_color": "#d51e1e", "capstyle": "butt", "colormap": "viridis", "contour_label_size": 12, "contour_line_color": "#000000", "contour_line_style": "-", "contour_line_width": 1, "contour_method": "exponential_kamb", "contour_resolution": 40, "contour_sigma": 2, "contour_use_line_color": true, "dip_rose_spacing": 10, "draw_angelier": true, "draw_contour_fills": false, "draw_contour_labels": false, "draw_contour_lines": false, "draw_fisher_sc": false, "draw_gcircles": true, "draw_hoeppener": false, "draw_linears": true, "draw_lp_plane": false, "draw_mean_vector": false, "draw_poles": false, "fisher_conf": 95, "label": "Linear Layer", "line_alpha": 1.0, "line_color": "#0000ff", "line_style": "-", "line_width": 1.0, "lower_limit": 1, "manual_range": false, "marker_alpha": 1.0, "marker_edge_color": "#000000", "marker_edge_width": 1.0, "marker_fill": "#69b3ff", "marker_size": 8.0, "marker_style": "o", "page": 1, "pole_alpha": 1.0, "pole_edge_color": "#000000", "pole_edge_width": 1.0, "pole_fill": "#1abd00", "pole_size": 8.0, "pole_style": "^", "rose_bottom": 0, "rose_spacing": 10, "steps": 10, "type": "line", "upper_limit": 10}, [[200.07497867994334, 30.732569990472655, ""]]]], "settings": {"canvas_color": "#bfbfbf", "draw_grid": true, "draw_legend": true, "equal_area_projection": true, "grid_color": "#787878", "grid_cutoff_lat": 80, "grid_linestyle": "--", "grid_width": 0.4, "highlight": false, "major_grid_spacing": 10, "minor_grid_spacing": 2, "pixel_density": 75, "show_cross": true, "show_north": true}}"""
    reset_project()
    store, lyr_obj_new = gui.on_toolbutton_create_plane_dataset_clicked(widget=None)
    gui.add_planar_feature(store, 140, 50, "")
    store, lyr_obj_new = gui.on_toolbutton_create_plane_dataset_clicked(widget=None)
    gui.add_planar_feature(store, 270, 60, "")
    selection = gui.layer_view.get_selection()
    selection.select_all()
    gui.on_toolbutton_plane_intersect_clicked(widget=None)
    data = gui.on_toolbutton_save_clicked(widget=None, testing=True)
    assert data == lyr_copy

def test_best_fit_plane():
    """
    Calculates the best-fit-plane of a set a linears. Asserts the project serialization.
    """
    lyr_copy = """{"filetype": "InnStereo data file 1.0", "layers": [["0", {"arrow_color": "#d51e1e", "capstyle": "butt", "colormap": "viridis", "contour_label_size": 12, "contour_line_color": "#000000", "contour_line_style": "-", "contour_line_width": 1, "contour_method": "exponential_kamb", "contour_resolution": 40, "contour_sigma": 2, "contour_use_line_color": true, "dip_rose_spacing": 10, "draw_angelier": true, "draw_contour_fills": false, "draw_contour_labels": false, "draw_contour_lines": false, "draw_fisher_sc": false, "draw_gcircles": true, "draw_hoeppener": false, "draw_linears": true, "draw_lp_plane": false, "draw_mean_vector": false, "draw_poles": false, "fisher_conf": 95, "label": "Linear Layer", "line_alpha": 1.0, "line_color": "#0000ff", "line_style": "-", "line_width": 1.0, "lower_limit": 1, "manual_range": false, "marker_alpha": 1.0, "marker_edge_color": "#000000", "marker_edge_width": 1.0, "marker_fill": "#69b3ff", "marker_size": 8.0, "marker_style": "o", "page": 1, "pole_alpha": 1.0, "pole_edge_color": "#000000", "pole_edge_width": 1.0, "pole_fill": "#1abd00", "pole_size": 8.0, "pole_style": "^", "rose_bottom": 0, "rose_spacing": 10, "steps": 10, "type": "line", "upper_limit": 10}, [[250.0, 30.0, ""], [140.0, 20.0, ""]]], ["1", {"arrow_color": "#d51e1e", "capstyle": "butt", "colormap": "viridis", "contour_label_size": 12, "contour_line_color": "#000000", "contour_line_style": "-", "contour_line_width": 1, "contour_method": "exponential_kamb", "contour_resolution": 40, "contour_sigma": 2, "contour_use_line_color": true, "dip_rose_spacing": 10, "draw_angelier": true, "draw_contour_fills": false, "draw_contour_labels": false, "draw_contour_lines": false, "draw_fisher_sc": false, "draw_gcircles": true, "draw_hoeppener": false, "draw_linears": true, "draw_lp_plane": false, "draw_mean_vector": false, "draw_poles": false, "fisher_conf": 95, "label": "Plane Layer", "line_alpha": 1.0, "line_color": "#0000ff", "line_style": "-", "line_width": 1.0, "lower_limit": 1, "manual_range": false, "marker_alpha": 1.0, "marker_edge_color": "#000000", "marker_edge_width": 1.0, "marker_fill": "#ff7a00", "marker_size": 8.0, "marker_style": "o", "page": 0, "pole_alpha": 1.0, "pole_edge_color": "#000000", "pole_edge_width": 1.0, "pole_fill": "#1abd00", "pole_size": 8.0, "pole_style": "^", "rose_bottom": 0, "rose_spacing": 10, "steps": 10, "type": "plane", "upper_limit": 10}, [[204.01898733956048, 39.72126963367138, ""]]]], "settings": {"canvas_color": "#bfbfbf", "draw_grid": true, "draw_legend": true, "equal_area_projection": true, "grid_color": "#787878", "grid_cutoff_lat": 80, "grid_linestyle": "--", "grid_width": 0.4, "highlight": false, "major_grid_spacing": 10, "minor_grid_spacing": 2, "pixel_density": 75, "show_cross": true, "show_north": true}}"""
    reset_project()
    store, lyr_obj_new = gui.on_toolbutton_create_line_dataset_clicked(widget=None)
    gui.add_linear_feature(store, 250, 30, "")
    gui.add_linear_feature(store, 140, 20, "")
    selection = gui.layer_view.get_selection()
    selection.select_all()
    gui.on_toolbutton_best_plane_clicked(widget=None)
    data = gui.on_toolbutton_save_clicked(widget=None, testing=True)
    assert data == lyr_copy

def test_mean_vector():
    """
    Calculates the mean vector of a set a linears. Asserts the project serialization.
    """
    lyr_copy = """{"filetype": "InnStereo data file 1.0", "layers": [["0", {"arrow_color": "#d51e1e", "capstyle": "butt", "colormap": "viridis", "contour_label_size": 12, "contour_line_color": "#000000", "contour_line_style": "-", "contour_line_width": 1, "contour_method": "exponential_kamb", "contour_resolution": 40, "contour_sigma": 2, "contour_use_line_color": true, "dip_rose_spacing": 10, "draw_angelier": true, "draw_contour_fills": false, "draw_contour_labels": false, "draw_contour_lines": false, "draw_fisher_sc": false, "draw_gcircles": true, "draw_hoeppener": false, "draw_linears": true, "draw_lp_plane": false, "draw_mean_vector": false, "draw_poles": false, "fisher_conf": 95, "label": "Linear Layer", "line_alpha": 1.0, "line_color": "#0000ff", "line_style": "-", "line_width": 1.0, "lower_limit": 1, "manual_range": false, "marker_alpha": 1.0, "marker_edge_color": "#000000", "marker_edge_width": 1.0, "marker_fill": "#69b3ff", "marker_size": 8.0, "marker_style": "o", "page": 1, "pole_alpha": 1.0, "pole_edge_color": "#000000", "pole_edge_width": 1.0, "pole_fill": "#1abd00", "pole_size": 8.0, "pole_style": "^", "rose_bottom": 0, "rose_spacing": 10, "steps": 10, "type": "line", "upper_limit": 10}, [[45.0, 30.0, ""], [60.0, 40.0, ""], [55.0, 20.0, ""]]], ["1", {"arrow_color": "#d51e1e", "capstyle": "butt", "colormap": "viridis", "contour_label_size": 12, "contour_line_color": "#000000", "contour_line_style": "-", "contour_line_width": 1, "contour_method": "exponential_kamb", "contour_resolution": 40, "contour_sigma": 2, "contour_use_line_color": true, "dip_rose_spacing": 10, "draw_angelier": true, "draw_contour_fills": false, "draw_contour_labels": false, "draw_contour_lines": false, "draw_fisher_sc": false, "draw_gcircles": true, "draw_hoeppener": false, "draw_linears": true, "draw_lp_plane": false, "draw_mean_vector": false, "draw_poles": false, "fisher_conf": 95, "label": "Mean Vector", "line_alpha": 1.0, "line_color": "#0000ff", "line_style": "-", "line_width": 1.0, "lower_limit": 1, "manual_range": false, "marker_alpha": 1.0, "marker_edge_color": "#000000", "marker_edge_width": 1.0, "marker_fill": "#ff7a00", "marker_size": 8.0, "marker_style": "o", "page": 1, "pole_alpha": 1.0, "pole_edge_color": "#000000", "pole_edge_width": 1.0, "pole_fill": "#1abd00", "pole_size": 8.0, "pole_style": "^", "rose_bottom": 0, "rose_spacing": 10, "steps": 10, "type": "eigenvector", "upper_limit": 10}, [[53.12603208349311, 30.142463315485486, 0.9856301083048257]]]], "settings": {"canvas_color": "#bfbfbf", "draw_grid": true, "draw_legend": true, "equal_area_projection": true, "grid_color": "#787878", "grid_cutoff_lat": 80, "grid_linestyle": "--", "grid_width": 0.4, "highlight": false, "major_grid_spacing": 10, "minor_grid_spacing": 2, "pixel_density": 75, "show_cross": true, "show_north": true}}"""
    reset_project()
    store, lyr_obj_new = gui.on_toolbutton_create_line_dataset_clicked(widget=None)
    gui.add_linear_feature(store, 45, 30, "")
    gui.add_linear_feature(store, 60, 40, "")
    gui.add_linear_feature(store, 55, 20, "")
    selection = gui.layer_view.get_selection()
    selection.select_all()
    gui.on_toolbutton_mean_vector_clicked(toolbutton=None)
    data = gui.on_toolbutton_save_clicked(widget=None, testing=True)
    assert data == lyr_copy
