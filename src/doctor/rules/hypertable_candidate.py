"""Rule to find hypertable candidates.

This rule will find all tables in a database that are candidates for
turning into a hypertable.
"""

QUERY = """
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

from . import rule

@rule(__name__)
def check_rule(cursor):
    """Table might benefit from being transformed to a hypertable.

    1. The table '{table}' has a column '{colname}' of timestamp type '{coltype}'
    2. The table '{table}' is not partitioned
    3. There are index scans done on '{table}'
    4. There are rows in '{table}'
    5. There are more than 10 pages allocated to '{table}'.
    """
    cursor.execute(QUERY)
