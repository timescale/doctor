Timescale Database Doctor
=========================

Rule-based recommendations about your timeseries database.

Installation
------------

You can install ``timescale-doctor`` using ``pip``::

  pip install timescale-doctor

Running the tool
----------------

Just call it in a similar manner to how ``psql`` is called::

  timescale-doctor my_database

It understands the usual environment variables `PGUSER`, `PGHOST`,
`PGDATABASE`, etc. Note that it do *not* understand PostgreSQL URLs
yet. See `Support PostgreSQL URLs for connection
<https://github.com/timescale/doctor/issues/5>`_.

Rules that are checked
----------------------

The Doctor currently has the following rules:

* `index.UnusedIndex`: If an index is unused, it can likely be
  removed. This will (of course) generate a false positive for
  databases that have not seen a lot of active use.

* `hypertable.HypertableCandidate`: Detect tables that can be turned
  into a hypertable. This is mostly beneficial for large tables, but
  this rule checks if there are 10 pages or more, which is kind of
  arbitrary.

* `hypertable.ChunkPermissions`: Check that all chunks have
  permissions that are compatible with the hypertable. If that is not
  the case, strange errors can be generated for queries on the table.

* `compression.LinearSegmentBy`: If a compressed table uses a
  segment-by column that increases linearly with rows added, it is
  probably not a good choice for segment-by.

* `compression.PointlessSegmentBy`: If the compressed table is using a
  column that is estimated to have a single value, it is usually
  pointless to use as a segment-by.


Writing new rules
-----------------

Instructions for writing new rules are available in the `README in the
rules package <src/doctor/rules/README.rst>`_.

License
-------

Copyright 2023 Timescale, Inc.

Licensed under the Apache License, Version 2.0 (the "License"); you
may not use this file except in compliance with the License.  You may
obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
implied.  See the License for the specific language governing
permissions and limitations under the License.
