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

"""Unit tests for compressed hypertable rules."""

from os.path import join, dirname

from doctor.rules.hypertable import ChunkPermissions
from doctor.unittest import TimescaleDBTestCase

class TestHypertableRules(TimescaleDBTestCase):
    """Test hypertable rules."""

    def setUp(self):
        """Set up unit tests for hypertable rules."""
        print(__file__)
        fname = join(dirname(__file__), "sql/setup.hypertable_test.sql")
        with self.connection.cursor() as cursor, open(fname, "r", encoding="ascii") as infile:
            cursor.execute(infile.read())

    def tearDown(self):
        """Tear down compression rules test."""
        fname = join(dirname(__file__), "sql/teardown.hypertable_test.sql")
        with self.connection.cursor() as cursor, open(fname, "r", encoding="ascii") as infile:
            cursor.execute(infile.read())

    def test_chunk_permissions(self):
        """Test chunk permission rule."""
        with self.connection.cursor() as cursor:
            cursor.execute(
                "SELECT chunk FROM show_chunks(%s) AS chunk ORDER BY chunk LIMIT 1",
                ('conditions',)
            )
            row = cursor.fetchone()
            self.assertIsNotNone(row)
            cursor.execute(f"REVOKE SELECT ON {row['chunk']} FROM PUBLIC")
        messages = []
        messages.extend(self.run_rule(ChunkPermissions()))
        message = ChunkPermissions.message.format(chunk=row['chunk'], hypertable="conditions")
        self.assertIn(message, messages)
