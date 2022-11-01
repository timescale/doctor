"""Rule-based recommendations for timeseries databases.

This tool will provide recommendations regarding your timeseries
database.
"""

import argparse
import os

from . import rules

__version__ = "0.0.1"

def parse_arguments():
    """Parse arguments to command-line tool."""
    parser = argparse.ArgumentParser(description=__doc__, add_help=False)
    parser.add_argument('-U', '--username', dest='user',
                        default=(os.getenv("PGUSER") or os.getlogin()),
                        help='user name to connect as')
    parser.add_argument('-d', '--dbname', metavar='DBNAME', dest='dbname',
                        help='name of the database to connect to')
    parser.add_argument('dbname', metavar='DBNAME', nargs='?',
                        default=(os.getenv("PGDATABASE") or os.getlogin()),
                        help='name of the database to connect to')
    parser.add_argument('-p', '--port', metavar='PORT', default='5432',
                        help='database server port number')
    parser.add_argument('-h', '--host', metavar='HOSTNAME',
                        help='database server host or socket directory')
    parser.add_argument('--help', action='help', default=argparse.SUPPRESS,
                        help='show this help message and exit')
    parser.add_argument("--verbose", "-v", dest="log_level",
                        action="count", default=2,
                        help='Verbose logging. More options give higher verbosity.')
    return parser.parse_args()

def main():
    """Run application."""
    args = parse_arguments()
    rules.check_rules(user=args.user, dbname=args.dbname, port=args.port, host=args.host)
