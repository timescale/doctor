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

import os
import unittest
import psycopg2

from psycopg2.extras import RealDictCursor
from timescaledb import Hypertable

from doctor.rules.compression import LinearSegmentBy, PointlessSegmentBy

class TestCompressionRules(unittest.TestCase):
    """Test compression rules.

    This will create a hypertable where we segment-by a column that
    has unique values (the time column) and a column that has only a
    single value (user_id).

    """

    def setUp(self):
        """Set up unit tests for compression rules."""
        user = (os.getenv("PGUSER") or os.getlogin())
        host = os.getenv("PGHOST")
        port = os.getenv("PGPORT") or "5432"
        dbname = (os.getenv("PGDATABASE") or os.getlogin())
        self.__conn = psycopg2.connect(dbname=dbname, user=user, host=host, port=port,
                                       cursor_factory=RealDictCursor)
        table = Hypertable("conditions", "time", {
                           'time': "timestamptz not null",
                           'device_id': "integer",
                           'user_id': "integer",
                           'temperature': "float"
        })
        table.create(self.__conn)

        with self.__conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO conditions "
                "SELECT time, (random()*30)::int, 1, random()*80 - 40 "
                "FROM generate_series(NOW() - INTERVAL '6 days', NOW(), '1 minute') AS time"
            )
            cursor.execute(
                "ALTER TABLE conditions SET ("
                "    timescaledb.compress,"
                "    timescaledb.compress_segmentby = 'time, user_id'"
                ")"
                )
            cursor.execute("ANALYZE conditions")
        self.__conn.commit()

    def tearDown(self):
        """Tear down compression rules test."""
        with self.__conn.cursor() as cursor:
            cursor.execute("DROP TABLE conditions")
        self.__conn.commit()

    def run_rule(self, rule):
        """Run rule and return messages."""
        return rule.execute(self.__conn, rule.message)

    def test_segmentby(self):
        """Test rule for detecting bad choice for segment-by column."""
        messages = []
        messages.extend(self.run_rule(LinearSegmentBy()))
        messages.extend(self.run_rule(PointlessSegmentBy()))
        self.assertIn(LinearSegmentBy.message.format(attname="time", relation="conditions"),
                      messages)
        self.assertIn(PointlessSegmentBy.message.format(attname="user_id", relation="conditions"),
                      messages)
