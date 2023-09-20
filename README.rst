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
