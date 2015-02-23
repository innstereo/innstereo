#!/usr/bin/python3

"""
This module imports a function to start the program and executes it.

The startup function calls the Gtk.Builder, parses the Glade-file,
creates and instance of the MainWindow class, connects the signals
and starts the Gtk main loop.
"""

from main_ui import startup


startup()
