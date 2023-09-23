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

"""Rules for hypertables."""

import doctor

CANDIDATE_QUERY = """
SELECT relid::regclass AS table,
       pt.typname AS coltype,
       psui.idx_scan,
       attname AS colname
  FROM pg_catalog.pg_stat_user_indexes AS psui
  LEFT JOIN pg_catalog.pg_inherits ON (inhparent=relid OR inhrelid=relid)
  JOIN pg_catalog.pg_index USING (indexrelid)
  JOIN pg_catalog.pg_attribute ON (attrelid=relid AND attnum=ANY(indkey))
  JOIN pg_catalog.pg_type AS pt ON (atttypid=pt.oid)
  JOIN pg_catalog.pg_stat_user_tables AS psut USING (relid)
  JOIN pg_catalog.pg_class AS pc ON (pc.oid=relid)
  JOIN pg_catalog.pg_class AS pci ON (pci.oid=indexrelid)
  WHERE pg_inherits IS NULL
    AND pt.typname IN ('timestamp', 'timestamptz')
    AND psui.idx_scan > 0
    AND n_live_tup + n_dead_tup > 0
    AND pc.relpages > 10;
"""

CANDIDATE_DETAIL = """
Table might benefit from being transformed to a hypertable.

1. The table '{table}' has a column '{colname}' of timestamp type '{coltype}'
2. The table '{table}' is not partitioned
3. There are index scans done on '{table}'
4. There are rows in '{table}'
5. There are more than 10 pages allocated to '{table}'.
"""

@doctor.register
class HypertableCandidate(doctor.Rule):
    """Detect candidate hypertable."""

    query: str = CANDIDATE_QUERY
    detail: str = CANDIDATE_DETAIL
    message: str = "Table {table} might benefit from being transformed to a hypertable."

PERMISSION_QUERY = """
WITH tables AS (
    SELECT format('%I.%I', ht.schema_name, ht.table_name)::regclass as hypertable,
           format('%I.%I', ch.schema_name, ch.table_name)::regclass as chunk
      FROM _timescaledb_catalog.hypertable ht
      JOIN _timescaledb_catalog.chunk ch
        ON ch.hypertable_id = ht.id
     WHERE NOT dropped)
SELECT hypertable,
       chunk
  FROM tables
 WHERE (SELECT relacl FROM pg_class WHERE oid = hypertable)
       IS DISTINCT FROM (SELECT relacl FROM pg_class WHERE oid = chunk);
"""

@doctor.register
class ChunkPermissions(doctor.Rule):
    """Detect bad chunk permissions."""

    query: str = PERMISSION_QUERY
    message: str = "Chunk '{chunk}' have different permissions from hypertable '{hypertable}'."
    dependencies: dict = {
        'timescaledb': '1.0'
    }
