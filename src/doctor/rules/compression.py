"""Rules for compressed hypertables."""

from . import rule

LINEAR_QUERY = """
SELECT format('%I.%I', schema_name, table_name)::regclass AS relation, s.attname
  FROM _timescaledb_catalog.hypertable_compression c
  JOIN _timescaledb_catalog.hypertable h ON c.hypertable_id = h.id
  JOIN pg_stats s
    ON s.attname = c.attname
   AND s.schemaname = h.schema_name
   AND s.tablename = h.table_name
 WHERE segmentby_column_index IS NOT NULL AND n_distinct < 0;
"""

@rule(__name__)
def linear_segmentby(cursor):
    """Column '{attname}' in hypertable '{relation}' as segment-by column is probably not a good choice since the number of values seems to grow with the number of rows of the table."""
    cursor.execute(LINEAR_QUERY)

POINTLESS_QUERY = """
SELECT format('%I.%I', schema_name, table_name)::regclass AS relation, s.attname
  FROM _timescaledb_catalog.hypertable_compression c
  JOIN _timescaledb_catalog.hypertable h ON c.hypertable_id = h.id
  JOIN pg_stats s
    ON s.attname = c.attname
   AND s.schemaname = h.schema_name
   AND s.tablename = h.table_name
 WHERE segmentby_column_index IS NOT NULL AND n_distinct = 1;
"""

@rule(__name__)
def pointless_segmentby(cursor):
    """Column '{attname}' in hypertable '{relation}' as segment-by column is pointless since it contains a single value."""
    cursor.execute(POINTLESS_QUERY)
    
