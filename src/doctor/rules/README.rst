Timescale Database Doctor Rules
===============================

You can define your own rule for querying the database by adding a new
file in this directory. The installation will automatically pick up
any files added to this directory.

The ``__init__.py`` file defines some basic support functions, in
particular the `register` decorator and the `Rule` class that you use
to create a new rule:

.. code-block:: python

   UNUSED_QUERY = """
   SELECT relid::regclass as relation,
	  indexrelname,
	  pg_size_pretty(pg_relation_size(i.indexrelid)) AS index_size
   FROM pg_stat_user_indexes ui JOIN pg_index i USING (indexrelid)
   WHERE NOT indisunique AND idx_scan = 0;
   """

   UNUSED_DETAIL = """
   Since index {indexrelname} in table {relation} is not used, you can
   remove it without affecting performance.
   """

   import doctor

   @doctor.register
   @dataclass
   class UnusedIndex(doctor.Rule):
      """Find all unused indexes."""

      query: str = UNUSED_QUERY
      message: str = "Index {indexrelname} in table {relation} is not used."
      hint: str = UNUSED_DETAIL

The module name is used as the category for the checks (the
``__module__`` parameter of the class), and the class name is used as
the name of the check. Assuming that the rule is present in the file
``index.py`` (with module name ``index``), then you will be able to
refer to this rule using ``index.UnusedIndex``.

Each rule can define the following fields:

*query*
  The SQL query to execute. This is a required field.

*message*
  The message to show for each object. This is a required field.

*detail*
  A more elaborate message to show containing more information about
  why the message is shown. This is an optional field. If no field is
  given, the value of the `message` field will be used.

*hint*
  A hint with how the warning can be eliminated. This is an optional
  field. If no field is given, the value of the `message` field will
  be used.

All the text messages are formatted using the named version of the
result set, so you can refer to columns in the result set using in the
same manner as for `formatted string literals`_. Note that there is
one message generated for each row of the result set, which are then
combined into a list.

.. _formatted string literals: https://docs.python.org/3/reference/lexical_analysis.html#f-strings
