"""Rule-based recommendations for timeseries databases.

This tool will provide recommendations regarding your timeseries
database.
"""

from textwrap import dedent, fill
from os.path import dirname, basename, isfile, join
from abc import ABC

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

    """

    def execute(self, conn, text):
        """Execute rule and return one string for each mismatching object."""
        cursor = conn.cursor()
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

__version__ = "0.0.1"
