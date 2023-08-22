"""Rules to check for a database.

This is the package containing all rules. To add an additional rule,
add a separate file to this directory and define any rules you deem
necessary.

"""

import glob
import importlib

from os.path import dirname, basename, isfile, join

def load_rules():
    """Load all rules from package."""
    # Add all files in this directory to be loaded, except __init__.py
    modules = [
        basename(f)[:-3] for f in glob.glob(join(dirname(__file__), "*.py"))
        if isfile(f) and not f.endswith('__init__.py')
    ]
    for module in modules:
        importlib.import_module(f".{module}", __name__)
