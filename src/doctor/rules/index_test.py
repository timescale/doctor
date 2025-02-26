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

"""Unit tests for index checking rules."""

from timescaledb import Table

from doctor.unittest import PostgreSQLTestCase
from doctor.rules.index import DuplicateIndex, UnusedIndex

class TestIndexRules(PostgreSQLTestCase):
    """Test index checking rules."""

    def setUp(self):
        """Set up unit tests for index checking rules."""
        table = Table("with_duplicate_index", {
            "one": "int",
            "two": "int",
        })
        table.create(self.connection)

        Table("my_table", {
            "time": "TIMESTAMPTZ NOT NULL",
            "device": "INTEGER",
            "temperature": "FLOAT",
        }).create(self.connection)

        with self.connection.cursor() as cursor:
            cursor.execute("CREATE INDEX index_one ON with_duplicate_index(one,two)")
            cursor.execute("CREATE INDEX index_two ON with_duplicate_index(one,two)")
            cursor.execute("CREATE INDEX my_index ON my_table(device)")
        self.connection.commit()

    def tearDown(self):
        """Tear down unit tests for index checking rules."""
        with self.connection.cursor() as cursor:
            cursor.execute("DROP TABLE with_duplicate_index")
            cursor.execute("DROP TABLE my_table")
        self.connection.commit()

    def test_duplicate(self):
        """Test rule for detecting duplicate index."""
        messages = []
        messages.extend(self.run_rule(DuplicateIndex()))
        self.assertIn(DuplicateIndex.message.format(index1="index_one", index2="index_two"),
                      messages)

    def test_unused_index(self):
        """Test unused index rule."""
        messages = []
        messages.extend(self.run_rule(UnusedIndex()))
        message = UnusedIndex.message.format(indexrelname='my_index', relation='my_table')
        self.assertIn(message, messages)
