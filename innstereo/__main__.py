#!/usr/bin/python3

"""
This module imports the main program and executes it.

The __init__ module just imports the main program module (main_ui).
The main program is then launched using the imported startup-function.
"""

import os.path
from .main_ui import startup

startup()

