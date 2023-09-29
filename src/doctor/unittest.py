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

"""Unit tests support for Timescale Doctor rules.

"""

import os
import unittest

from abc import ABCMeta

import psycopg2

from psycopg2.extras import RealDictCursor
from testcontainers.postgres import PostgresContainer

class TestCase(unittest.TestCase, metaclass=ABCMeta):
    """Base class for Timescale Doctor unit tests.

    Test cases are executed in a container that depends on the
    requirements of the test case. Subclasses of this class add the
    actual container and is the test case class that should be used.

    """

    container_name = None

    @property
    def connection(self):
        """Get database connection."""
        return self.__connection

    @property
    def container(self):
        """Get container the test is running in."""
        return self.__container

    def run_rule(self, rule):
        """Run rule and return messages."""
        return rule.execute(self.connection, rule.message)

    @classmethod
    def setUpClass(cls):
        """Start a container and create a connection for all tests."""
        assert cls.container_name is not None
        cls.__container = PostgresContainer(cls.container_name).start()
        connstring = cls.__container.get_connection_url().replace("+psycopg2", "")
        cls.__connection = psycopg2.connect(connstring, cursor_factory=RealDictCursor)

    @classmethod
    def tearDownClass(cls):
        """Close the connection and stop the container."""
        cls.__connection.close()
        cls.__container.stop()

class TimescaleDBTestCase(TestCase):
    """Base class for test cases that need TimescaleDB.

    It will read the container name from the environment variable
    "TEST_CONTAINER_TIMESCALE" if present, or default to
    "timescaledb:latest-pg15".

    Typical usage::

        from doctor.unittest import TimescaleDBTestCase

        class TestCompressionRules(TimescaleDBTestCase):
            ...

    """

    container_name = os.environ.get('TEST_CONTAINER_TIMESCALE', 'timescale/timescaledb:latest-pg15')

class PostgreSQLTestCase(TestCase):
    """Base class for test cases that use plain PostgreSQL.

    It will read the container name from the environment variable
    "TEST_CONTAINER_POSTGRES" if present, or default to
    "postgres:latest".

    Typical usage::

        from doctor.unittest import PostgreSQLTestCase

        class TestCompressionRules(PostgreSQLTestCase):
            ...
    """

    container_name = os.environ.get('TEST_CONTAINER_POSTGRES', 'postgres:latest')
