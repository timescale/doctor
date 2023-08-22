"""Rules for indexes."""

from dataclasses import dataclass

import doctor

UNUSED_QUERY = """
SELECT relid::regclass as relation,
       indexrelname,
       pg_size_pretty(pg_relation_size(i.indexrelid)) AS index_size
FROM pg_stat_user_indexes ui JOIN pg_index i USING (indexrelid)
WHERE NOT indisunique
  AND idx_scan = 0
  AND schemaname NOT LIKE '_timescaledb%';
"""

@doctor.register
@dataclass
class UnusedIndex(doctor.Rule):
    """Find all unused indexes."""

    query: str = UNUSED_QUERY
    message: str = "index '{indexrelname}' on table '{relation}' is not used"
    detail: str = "Index {indexrelname} is not used and occupied {index_size}."
    hint: str = ("Since the index '{indexrelname}' on table '{relation}' is not used,"
                 " you can remove it.")
