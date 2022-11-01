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
