"""Rules for indexes."""

from . import rule

QUERY = """
SELECT relname,
       indexrelname,
       pg_size_pretty(pg_relation_size(i.indexrelid)) AS index_size
FROM pg_stat_user_indexes ui JOIN pg_index i USING (indexrelid)
WHERE NOT indisunique AND idx_scan = 0;
"""

@rule(__name__)
def unused(cursor):
    """Index '{indexrelname}' on table '{relname}' is not used.

    Consider removing it and saving {index_size}.

    """
    cursor.execute(QUERY)
