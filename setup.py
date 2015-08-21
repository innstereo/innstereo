from distutils.core import setup
from os import path

pjoin = path.join

setup(
    name = "innstereo",
    version = "1.0-b2",
    description = "Sterographic plotting for structural geology",
    author = "Tobias Schoenberg",
    author_email = "tobias47n9e@gmail.com",
    license = "GPL2",
    url = "https://github.com/tobias47n9e/innstereo",
    keywords = ["geology", "stereonet", "structural geology"],
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: Pre-Alpha",
        "Environment :: Other Environment",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering",
        ],
    packages = ["innstereo"],
    scripts = [pjoin("bin","innstereo.py")],
    install_requires = ["numpy >= 1.6.0",
                        "scipy >= 0.13",
                        "matplotlib >= 1.4.0",
                        "mplstereonet >= 0.4"],
    setup_requires = ["numpy >= 1.6.0",
                      "scipy >= 0.13",
                      "matplotlib >= 1.4.0",
                      "mplstereonet >= 0.4"],
    py_modules = [pjoin("innstereo","__init__"),
                  pjoin("innstereo","dataview_classes"),
                  pjoin("innstereo","dialog_windows"),
                  pjoin("innstereo","file_parser"),
                  pjoin("innstereo","layer_types"),
                  pjoin("innstereo","layer_view"),
                  pjoin("innstereo","main_ui"),
                  pjoin("innstereo","plot_control"),
                  pjoin("innstereo","polar_axes")],
    package_data = {"ibk_st": ["calculate_bestfit_points.svg",
                               "calculate_eigenvector.svg",
                               "calculate_plane_intersect.svg",
                               "calculate_poles_to_lines.svg",
                               "create_faultplane.svg",
                               "create_fold.svg",
                               "create_line.svg",
                               "create_plane.svg",
                               "create_small_circle.svg",
                               "logo_about.svg",
                               "gui_layout.glade"]},
    tests_require = "pytest",
    long_description = """
    Innstereo (or Innsbruck Stereographic) is an open-source stereographic
    projection program for structural geology and based on MPLStereonet. It can
    be used to create plots of geologic data and can perform a number of
    calculations on the datasets.
    """
    )
