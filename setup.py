from distutils.core import setup

setup(
    name = "innsbruck-stereographic",
    version = "1.0-a1",
    description = "Sterographic plotting for structural geology",
    author = "Tobias Schoenberg",
    author_email = "tobias47n9e@gmail.com",
    license = "GPL2",
    url = "https://github.com/tobias47n9e/innsbruck-stereographic",
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
    packages = ["ibk_st"],
    scripts = ["bin/innsbruck-stereographic"],
    install_requires = ["numpy >= 1.6.0",
                        "scipy >= 0.14",
                        "matplotlib >= 1.4.0",
                        "mplstereonet >= 0.4"],
    setup_requires = ["numpy >= 1.6.0",
                      "scipy >= 0.14",
                      "matplotlib >= 1.4.0",
                      "mplstereonet >= 0.4"],
    py_modules = ["__init__",
                  "dataview_classes",
                  "dialog_windows",
                  "file_parser",
                  "layer_types",
                  "layer_view",
                  "main_ui",
                  "plot_control",
                  "polar_axes"],
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
    long_description = """
    Innsbruck Stereographic is an open-source stereographic projection program
    for structural geology and based on MPLStereonet. It can be used to create
    plots of geologic data and can perform a number of calculations on the
    datasets.
    """
    )
