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

"""Rule-based recommendations for timeseries databases.

This tool will provide recommendations regarding your timeseries
database.
"""

from fnmatch import fnmatch
from textwrap import dedent, fill, TextWrapper
from os.path import dirname, basename, isfile, join
from abc import ABC
from packaging.version import parse

import psycopg2

from psycopg2.extras import RealDictCursor

# Rules are organized in a two-level hierarchy with the category as
# the top-level object and the functions below.
RULES = {}

# pylint: disable-next=too-few-public-methods
class Rule(ABC):
    """Superclass for all rules to check.

    This is an abstract base class (ABC) for all rules that are
    checked in the database. It contains some basic check that
    required fields exist.

    The following fields are available for the subclass:

    query: The SQL query to execute. This is a required field.

    message: The message to show for each object. This is a required
      field.

    detail: A more elaborate message to show containing more
      information about why the message is shown. This is an optional
      field. If no field is given, the value of the "message" field
      will be used.

    hint: A hint with how the warning can be eliminated. This is an
      optional field. If no field is given, the value of the "message"
      field will be used.

    dependencies: Dictionary with dependencies on packages and what
    versions that are required.

    """

    def get_versions(self, conn):
        """Get extension versions."""
        with conn.cursor() as cursor:
            cursor.execute("SELECT extname, extversion FROM pg_extension WHERE extname IN %s",
                           (tuple(self.dependencies.keys()),)) # pylint: disable=E1101
            return {row["extname"]: row["extversion"] for row in cursor}


    def execute(self, conn, text):
        """Execute rule and return one string for each mismatching object."""
        with conn.cursor() as cursor:
            # Check that all dependencies are met. If not, we do not
            # execute the rule.
            if hasattr(self, 'dependencies'):
                versions = self.get_versions(conn)
                for ext,req in self.dependencies.items(): # pylint: disable=E1101
                    if ext not in versions or parse(req) > parse(versions[ext]):
                        return []
            cursor.execute(self.query) # pylint: disable=E1101
            return [text.format(**kwrds) for kwrds in cursor]

def register(cls):
    """Register a rule."""
    if not hasattr(cls, 'query'):
        raise NameError('Class did not define a query', name='query')
    if not hasattr(cls, 'message'):
        raise NameError('Class did not define a message', name='message')
    category = cls.__module__.rpartition('.')[2]
    RULES.setdefault(category, {})[cls.__name__] = cls
    return cls


def list_rules(pattern, show):
    """List all rules matching pattern.

    Will list rules matching `pattern`, and print detailed message if
    `details` is true. Note that since the detailed message contains
    variables for expansion, and there is no replacements to use, the
    message with the placeholders will be printed.
    """
    wrapper = TextWrapper(initial_indent="    ", subsequent_indent="    ")
    for category, rules in RULES.items():
        for name, cls in rules.items():
            fullname = f"{category}.{name}"
            if fnmatch(fullname, pattern):
                print(f"{fullname}:")
                print(wrapper.fill(cls.__doc__))
                if show in ("details", "message"):
                    print("\n    == MESSAGE ==", end="\n\n")
                    print(wrapper.fill(cls.message), end="\n\n")
                    if show == "details" and hasattr(cls, 'detail'):
                        print(wrapper.fill(cls.detail), end="\n\n")

def check_rules(dbname, user, host, port):
    """Check all rules with the database."""
    conn = psycopg2.connect(dbname=dbname, user=user,
                            host=host, port=port,
                            cursor_factory=RealDictCursor)
    for category, rules in RULES.items():
        header_printed = False
        for _, cls in rules.items():
            rule = cls()
            for report in rule.execute(conn, rule.message):
                if not header_printed:
                    print(f"{category}:")
                    header_printed = True
                clean = dedent(report)
                print(fill(clean, initial_indent="- ", subsequent_indent="  "))
