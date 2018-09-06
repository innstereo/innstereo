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
]

install_data(innstereo_sources, install_dir: moduledir)