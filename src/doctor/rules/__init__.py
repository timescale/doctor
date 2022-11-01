"""Rules to check for a database.

This is the package containing all rules. To add an additional rule,
add a separate file to this directory and define any rules you deem
necessary.

"""

import psycopg2
import glob
import importlib

from os.path import dirname, basename, isfile, join
from psycopg2.extras import RealDictCursor

RULES = {}

class Rule:
    """Rule to check in database.

    The rule consists of a function that will retrieve a list of
    objects and print one message for each object. The rule text
    consists of a format string that will be using the columns
    mentioned in the query.

    The rules are most easily defined using the `rule` decorator
    below.

    The rule does not provide any specific requirements on the object
    that is being processed and it is entirely up to the rule logic to
    decide how to handle the result of the query. It is, however,
    assumed that no returned rows means that the rule does not
    identify any issues.

    """

    def __init__(self, func, text):
        """Initialize rule with function and template.
        
        Each rule consists of a function to call that will return a
        list of objects that fail the check and a template text that
        will be printed for each object.

        By default, the function documentation is used as the template
        text.

        """
        self.__func = func
        self.__text = func.__doc__ if text is None else text

    def check_and_report(self, conn):
        """Check rule and report mismatching objects.
        
        # Parameters

        conn: Connection to use when checking rule.
        """
        cursor = conn.cursor()
        self.__func(cursor)
        for kwrds in cursor:
            print(self.__text.format(**dict(kwrds)))


def rule(name):
    """Decorate rules.

    If you want to add a new rule to the system, put it in a separate
    file in this directory and use the decorator to define a new
    rule. If the rule returns any objects, the documentation string of
    the rule will be used as a template and printed once for each row.

    As an example, to define a rule 'reserved_prefix' that will
    trigger on any table name that starts with "ts_", you could use
    the following rule::

        @rule('reserved_prefix')
        def my_rule(cursor):
           'Table "{relname}" starts with the reserved prefix "ts_".'
           cursor.execute("SELECT relname FROM pg_class WHERE left(relname, 3) = 'ts_'")

    """

    def inner(func):
        func.name = name
        RULES[name] = Rule(func, func.__doc__)

    return inner

def check_rules(dbname, user, host, port):
    """Check all rules with the database.

    This will check all registered rules.
    """
    if host is None:
        host = '/tmp'

    conn = psycopg2.connect(dbname=dbname, user=user,
                            host=host, port=port,
                            cursor_factory=RealDictCursor)
    for name, rule in RULES.items():
        rule.check_and_report(conn)

# Add all files in this directory to be loaded, except __init__.py
modules = [
    basename(f)[:-3] for f in glob.glob(join(dirname(__file__), "*.py"))
    if isfile(f) and not f.endswith('__init__.py')
]
for module in modules:
    importlib.import_module(f".{module}", __name__)
