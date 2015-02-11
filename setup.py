from distutils.core import setup

setup(
    name = "innsbruck-stereographic",
    version = "0",
    description = "Sterographic plotting for structural geology",
    author = "Tobias Schoenberg",
    author_emial = "tobias47n9e@gmail.com",
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
    long_description = """
    Innsbruck Stereographic is a open-source stereographic projection program
    for structural geology and based on MPLStereonet. It can be used to create
    plots of geologic data and can perform a number of calculations on the
    datasets.
    """
    )
