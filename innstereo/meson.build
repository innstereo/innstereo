pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
moduledir = join_paths(pkgdatadir, 'innstereo')
gnome = import('gnome')

gnome.compile_resources('innstereo',
  'innstereo.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
)

python3 = import('python3')

conf = configuration_data()
conf.set('PYTHON', python3.find_python().path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', join_paths(get_option('prefix'), get_option('localedir')))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'innstereo.in',
  output: 'innstereo',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir')
)

innstereo_sources = [
  '__init__.py',
  '__main__.py',
  'main_ui.py',
  'dataview_classes.py',
  'i18n.py',
  'layer_view.py',
  'layer_types.py',
  'dialog_windows.py',
  'layer_properties.py',
  'plot_control.py',
  'polar_axes.py',
  'file_parser.py',
  'rotation_dialog.py',
  'viridis.py',
  'settings.py',
  'gui_layout.glade',
  'innstereo_icon_128.png',
  'calculate_poles_to_lines.svg',
  'rotate.svg',
  'calculate_pt_axis.svg',
  'calculate_plane_intersect.svg',
  'create_plane.svg',
  'create_line.svg',
  'create_fold.svg',
  'create_faultplane.svg',
  'calculate_mean_vector.svg',
  'calculate_normal_plane.svg',
  'calculate_fisher.svg',
  'calculate_eigenvector.svg',
  'create_small_circle.svg',
  'calculate_bestfit_points.svg',
]

install_data(innstereo_sources, install_dir: moduledir)