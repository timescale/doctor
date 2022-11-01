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
