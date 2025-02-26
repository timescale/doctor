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
import getpass
import os
import configparser

from doctor import check_rules, list_rules
from doctor.rules import load_rules


def parse_arguments():
    """Parse arguments to command-line tool."""
    parser = argparse.ArgumentParser(description=__doc__, add_help=False)
    parser.add_argument('-U', '--username', dest='user',
                        default=(os.getenv("PGUSER") or getpass.getuser()),
                        help='user name to connect as')
    parser.add_argument('-W', '--password', dest='password',
                        default=os.getenv("PGPASSWORD"),
                        help='Password to use when connecting')
    parser.add_argument('-s', '--service', metavar="NAME",
                        help="Service used. Read from ~/.pg_services.conf")
    parser.add_argument('-d', '--dbname', metavar='DBNAME', dest='dbname',
                        help='name of the database to connect to')
    parser.add_argument('dbname', metavar='DBNAME', nargs='?',
                        default=(os.getenv("PGDATABASE") or getpass.getuser()),
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
    parser.add_argument("--list", nargs='?', const='*', metavar="PATTERN",
                        default=argparse.SUPPRESS,
                        help=("List rules matching pattern. "
                              "If no pattern is given, will list all rules"))
    parser.add_argument('--sslmode', metavar='MODE',
                        default=os.getenv("PGSSLMODE"),
                        help='mode for negotiating SSL connection')
    parser.add_argument(
        '--show', choices=['brief', 'message', 'details'], default=None,
        help=("What to show from the rule. The brief description is always shown, "
              "but it is possible to show the message and the detailed message as "
              "well.")
    )

    args = parser.parse_args()

    if args.service is not None:
        config = configparser.ConfigParser()
        config.read(os.path.expanduser('~/.pg_service.conf'))
        args.host = config.get(args.service, 'host')
        args.port = config.get(args.service, 'port')
        args.user = config.get(args.service, 'user')
        args.password = config.get(args.service, 'password')
        args.dbname = config.get(args.service, 'dbname')
        args.sslmode = config.get(args.service, 'sslmode', fallback=None)

    return parser, args


def main():
    """Run application."""
    load_rules()
    parser, args = parse_arguments()
    if args.show and 'list' not in args:
        parser.error("called with '--show' but without '--list'")
    elif 'list' in args:
        if args.show is None:
            args.show = 'brief'
        list_rules(args.list, args.show)
    else:
        check_rules(args)
