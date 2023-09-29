# Copyright 2023 Timescale, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Rules to check for a database.

This is the package containing all rules. To add an additional rule,
add a separate file to this directory and define any rules you deem
necessary.
"""

import glob
import importlib

from os.path import dirname, basename, isfile, join

def is_rule_file(fname):
    """Check if file is a rules file."""
    if not isfile(fname):
        return False
    if fname.endswith(('__init__.py', '_test.py')) or fname.startswith("test_"):
        return False
    return True

def load_rules():
    """Load all rules from package."""
    # Add all files in this directory to be loaded, except __init__.py
    pyfiles = glob.glob(join(dirname(__file__), "*.py"))
    modules = [basename(f)[:-3] for f in pyfiles if is_rule_file(f)]
    for module in modules:
        importlib.import_module(f".{module}", __name__)
