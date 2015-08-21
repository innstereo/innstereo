#!/usr/bin/python3

import innstereo
from . import setup_json_strings


gui = innstereo.startup(testing=True)

setup_json_strings.run(gui)
