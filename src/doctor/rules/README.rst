Timescale Database Doctor Rules
===============================

You can define your own rule for querying the database by adding a new
file in this directory. The installation will automatically pick up
any files added to this directory.

The ``__init__.py`` file defines some basic support functions, in
particular the ``rule`` decorator that you can use to create a new
rule::

    QUERY = """
    SELECT relname,
	   indexrelname,
	       pg_size_pretty(pg_relation_size(i.indexrelid)) AS index_size,
	       idx_scan
    FROM pg_stat_user_indexes ui JOIN pg_index i USING (indexrelid)
    WHERE NOT indisunique AND idx_scan = 0;
    """

    from . import rule

    @rule(__name__)
    def unused(cursor):
      """These indexes are not used. You might consider removing them."""
      cursor.execute(QUERY)

The base name of each file is used as the category for the checks (the
``__name__`` parameter to the `rule` decorator), and the function name
is used as the name of the check. Assuming that the rule is present in
the file ``index.py``, then you will be able to refer to this rule using
``index.unused``.

Each rule will have a cursor passed in, allowing you to send a query
to the database and return a result set. The documentation string for
the function is used as a header for the result set and the
application will print the header and the result set in an easy to
read format.
