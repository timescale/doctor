Timescale Database Doctor
=========================

Rule-based recommendations about your timeseries database.

Installation
------------

To install this package, first make sure that you have a recent
version of ``setuptools``::

  pip install --upgrade setuptools

After that, you can use ``pip`` to install the package directly from
this directory::

  pip install .

The tool is installed as ``timescale-doctor``.

Running the tool
----------------

Just call it in a similar manner to how ``psql`` is called::

  timescale-doctor my_database

It understands the usual environment variables `PGUSER`, `PGHOST`, `PGDATABASE`, etc. Note that it do *not* understand
PostgreSQL URLs yet. See `Support PostgreSQL URLs for connection <https://github.com/timescale/doctor/issues/5>`_.

Writing new rules
-----------------

Instructions for writing new rules are available in the `README in the rules package <src/doctor/rules/README.rst>`_.
