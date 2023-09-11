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

"""Command-line interface to Timescale Doctor."""

import argparse
import os

from . import check_rules
from .rules import load_rules


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
    load_rules()
    args = parse_arguments()
    check_rules(user=args.user, dbname=args.dbname, port=args.port, host=args.host)
