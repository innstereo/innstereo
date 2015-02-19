<font color='red'>This program is currently under development. If you run Linux, or can run a Linux virtual machine you can participate in the testing and development. Please back up your data and use a safe testing environment!</font>

# Innsbruck Stereographic
Innsbruck Stereographic is an open-source program for stereographic projections or stereonets. It is developed for data processing in geology, structural-geology and related fields. The program itself is build on top of other open-source libraries, most importantly [MPLStereonet](https://github.com/joferkington/mplstereonet).

## Code metrics
Currently the code quality is monitored. Software testing will be implemented as soon as possible.

[![Code Health](https://landscape.io/github/tobias47n9e/innsbruck-stereographic/master/landscape.svg?style=flat)](https://landscape.io/github/tobias47n9e/innsbruck-stereographic/master)
[![Build Status](https://travis-ci.org/tobias47n9e/innsbruck-stereographic.svg)](https://travis-ci.org/tobias47n9e/innsbruck-stereographic)

## Installation
Builds for different operating systems will be done as soon as time permits. Currently the best way to test the program is to do the following on Linux or a Linux-Virtual-Machine. In both cases it is a good idea to test within a virtual environment:

1. Install the Python 3 packages of Matplotlib, Numpy, Git, etc...

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
python3 __init__.py
```

## Documentation
The latest documentation can be read on this page:

http://innsbruck-stereographic.readthedocs.org

[![Documentation Status](https://readthedocs.org/projects/innsbruck-stereographic/badge/?version=latest)](https://readthedocs.org/projects/innsbruck-stereographic/?badge=latest)

## Development
Innsbruck Stereographic is developed open-source, and anybody is welcome to participate. There are many ways in which to participate (Documentation, testing, bug-reporting, user-interface improvements). If you would like to participate you can email [Tobias](https://github.com/tobias47n9e) or open an [issue](https://github.com/tobias47n9e/innsbruck-stereographic/issues). More advanced users can also fork the repository and create pull requests.

## Known Issues
As this program is still in early development there are many known issues. In March 2015 this should be replaced by a more meaningful list.

## Digital Infrastructure
Innsbruck Stereographic is based on the following open-source libraries:

* [Glade](https://glade.gnome.org/)
* [GTK+](http://www.gtk.org/)
* [Matplotlib](http://matplotlib.org/)
* [MPLStereonet](https://github.com/joferkington/mplstereonet)
* [NumPy](http://www.numpy.org/)
