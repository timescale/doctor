"""Rules for compressed hypertables."""

from dataclasses import dataclass

import doctor

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

@doctor.register
@dataclass
class LinearSegmentby(doctor.Rule):
    """Detect segmentby column for compressed table."""

    query: str = LINEAR_QUERY
    message: str = (
        "Column '{attname}' in hypertable '{relation}' has no distinct values."
    )
    detail: str = (
        "Column '{attname}' in hypertable '{relation}' as segment-by column  is"
        " probably not a good choice since the number of values seems to grow"
        " with the number of rows of the table."
    )

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
@doctor.register
@dataclass
class PointlessSegmentBy(doctor.Rule):
    """Detect pointless segmentby column in compressed table."""

    query: str = POINTLESS_QUERY
    message: str = (
        "Column '{attname}' in hypertable '{relation}' as segment-by column is pointless"
    )
    detail: str = (
        "Column '{attname}' in hypertable '{relation}' as segment-by column is pointless"
        " since it contains a single value."
    )
