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

"""Utility functions for interacting with TimescaleDB."""

from abc import ABC, abstractmethod

# pylint: disable-next=too-few-public-methods
class SQL(ABC):
    """Superclass for objects in an SQL database."""

    @abstractmethod
    def create(self, conn):
        """Create the SQL object in the database."""

# pylint: disable-next=too-few-public-methods
class Table(SQL):
    """Class for a normal PostgreSQL table."""

    def __init__(self, name, columns):
        self.name = name
        self.columns = columns

    def create(self, conn):
        with conn.cursor() as cursor:
            coldefs = ",".join(f"{name} {defn}" for name, defn in self.columns.items())
            cursor.execute(f"CREATE TABLE {self.name} ({coldefs})")

# pylint: disable-next=too-few-public-methods
class Hypertable(Table):
    """Class for a TimescaleDB hypertable."""

    def __init__(self, name, partcol, columns):
        super().__init__(name, columns)
        self.partcol = partcol

    def create(self, conn):
        super().create(conn)
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM create_hypertable(%s, %s)",
                           (self.name, self.partcol))
