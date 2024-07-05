pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
moduledir = join_paths(pkgdatadir, 'facetracker')

conf = configuration_data()
conf.set('VERSION', meson.project_version())

python = import('python')
conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').full_path())
conf.set('APPID', 'de.zray.Facetracker')
conf.set('VERSION', meson.project_version())
conf.set('localedir', join_paths(get_option('prefix'), get_option('localedir')))
conf.set('pkgdatadir', pkgdatadir)

facetracer_bin = configure_file(
  input: '__init__.py',
  output: 'facetracker-gui',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir'),
  install_mode: 'r-xr-xr-x',
)

facetracker_sources = files([
    'const.py',
    'face_wrapper.py',
    'main_frame.py',
    'webcam_info.py'
])

install_data(facetracker_sources, install_dir: moduledir)