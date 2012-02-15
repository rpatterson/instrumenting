.. -*-doctest-*-

==========================
Regular Expression Filters
==========================

Start with a Python program we want to debug with ``pdb``.

    >>> from instrumenting import testing
    >>> testing.main
    <function main at 0x...>
    
Configure a pdb logging handler that does post_mortem debugging of
exceptions.

    >>> import logging
    >>> import instrumenting
    >>> root = logging.getLogger()
    >>> handler = instrumenting.PdbHandler()
    >>> root.addHandler(handler)

The regex filter can be used to filter log messages that match a
regular expression.

    >>> re_filter = instrumenting.ReFilter('Forced program exception')
    >>> handler.addFilter(re_filter)

    >>> testing.main()
    TESTING pdb.interaction() called: (<pdb.Pdb instance at 0x...>, None, <traceback object at 0x...>), {}
    >>> print testing_handler
    instrumenting.testing DEBUG
      debug message
    instrumenting.testing INFO
      info message
    instrumenting.testing WARNING
      warning message
    instrumenting.testing ERROR
      error message
    instrumenting.testing ERROR
      exception message: Forced program exception
    instrumenting.testing CRITICAL
      critical message
    >>> testing_handler.clear()

The handler can also be configured to log records that do *not* match
the expression.

    >>> handler.removeFilter(re_filter)
    >>> re_filter = instrumenting.ReFilter(
    ...     'Forced program exception', matched=False)
    >>> handler.addFilter(re_filter)

    >>> testing.main()
    TESTING pdb.set_trace() called: (<pdb.Pdb instance at 0x...>, <frame object at 0x...>), {}
    TESTING pdb.set_trace() called: (<pdb.Pdb instance at 0x...>, <frame object at 0x...>), {}
    >>> print testing_handler
    instrumenting.testing DEBUG
      debug message
    instrumenting.testing INFO
      info message
    instrumenting.testing WARNING
      warning message
    instrumenting.testing ERROR
      error message
    instrumenting.testing ERROR
      exception message: Forced program exception
    instrumenting.testing CRITICAL
      critical message
    >>> testing_handler.clear()

The filter can also be configured with a template to generate the
string the regex will be matched against based on arbitrary record
attributes.  For example, this could be used to match against the
logging frames source file and line number.

    >>> handler.removeFilter(re_filter)
    >>> code = testing.main.func_code
    >>> re_filter = instrumenting.ReFilter(
    ...     '%s:%s' % (code.co_filename, code.co_firstlineno+4),
    ...     format='%(pathname)s:%(lineno)d')
    >>> handler.addFilter(re_filter)

    >>> testing.main()
    TESTING pdb.set_trace() called: (<pdb.Pdb instance at 0x...>, <frame object at 0x...>), {}
    >>> print testing_handler
    instrumenting.testing DEBUG
      debug message
    instrumenting.testing INFO
      info message
    instrumenting.testing WARNING
      warning message
    instrumenting.testing ERROR
      error message
    instrumenting.testing ERROR
      exception message: Forced program exception
    instrumenting.testing CRITICAL
      critical message
    >>> testing_handler.clear()
