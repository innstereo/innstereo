# InnStereo
InnStereo (abbreviated from Innsbruck Stereographic) is an open-source program for stereographic projections, also called stereonets. It is developed for data processing in geology, structural-geology and related fields. The program itself is build on top of other open-source libraries, most importantly [MPLStereonet](https://github.com/joferkington/mplstereonet).

## Documentation
The latest documentation can be read on this page:

http://innsbruck-stereographic.readthedocs.org

[![Documentation Status](https://readthedocs.org/projects/innsbruck-stereographic/badge/?version=latest)](https://readthedocs.org/projects/innsbruck-stereographic/?badge=latest)

## Installation

Check the [releases page](https://github.com/tobias47n9e/innsbruck-stereographic/releases) for builds for your system:

## Development Version

Currently the best way to test the program is to do the following on Linux or a Linux-Virtual-Machine. In both cases it is a good idea to test within a virtual environment:

1. Install the Python 3 packages of Matplotlib, Numpy, Git, Scipy.

2. Download the newest version of MPLStereonet:
```Shell
pip3 install git+git://github.com/joferkington/mplstereonet.git
```
3. Clone this repository:
```Shell
git clone https://github.com/tobias47n9e/innsbruck-stereographic
```
4. Run the program by executing:
```Shell
python3 -m innstereo
```
in the project directory.

## Development
InnStereo is developed open-source, and anybody is welcome to participate. There are many ways in which to participate (Documentation, testing, bug-reporting, user-interface improvements). If you would like to participate you can email [Tobias](https://github.com/tobias47n9e) or open an [issue](https://github.com/tobias47n9e/innsbruck-stereographic/issues). More advanced users can also fork the repository and create pull requests.

## Known Issues
The program is still in development and some features are still missing. The most important things are listed in this file:

[Known issues](https://github.com/tobias47n9e/innsbruck-stereographic/blob/master/known_issues.rst)

## Digital Infrastructure
InnStereo is based on the following open-source projects:

* [Glade](https://glade.gnome.org/)
* [GTK+](http://www.gtk.org/)
* [Matplotlib](http://matplotlib.org/)
* [MPLStereonet](https://github.com/joferkington/mplstereonet)
* [NumPy](http://www.numpy.org/)
* [SciPy](http://www.scipy.org/)
* [Pynsist](https://github.com/takluyver/pynsist)

## Code Metrics
The code quality is constantly monitored using Landscape. Software-testing will be implemented as soon as possible.

[![Code Health](https://landscape.io/github/tobias47n9e/innsbruck-stereographic/master/landscape.svg?style=flat)](https://landscape.io/github/tobias47n9e/innsbruck-stereographic/master)
[![Build Status](https://travis-ci.org/tobias47n9e/innsbruck-stereographic.svg)](https://travis-ci.org/tobias47n9e/innsbruck-stereographic)
