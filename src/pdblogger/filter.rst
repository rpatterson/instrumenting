.. -*-doctest-*-

==========================
Regular Expression Filters
==========================

Start with a Python program we want to debug with ``pdb``.

    >>> from pdblogger import testing
    >>> testing.main
    <function main at 0x...>
    
Configure a pdb logging handler that does post_mortem debugging of
exceptions.

    >>> import logging
    >>> import pdblogger
    >>> root = logging.getLogger()
    >>> handler = pdblogger.PdbHandler()
    >>> root.addHandler(handler)

The regex filter can be used to filter log messages that match a
regular expression.

    >>> re_filter = pdblogger.ReFilter('Forced program exception')
    >>> handler.addFilter(re_filter)

    >>> testing.main()
    TESTING pdb.interaction() called: (<pdb.Pdb instance at 0x...>, None, <traceback object at 0x...>), {}
    >>> print testing_handler
    pdblogger.testing DEBUG
      debug message
    pdblogger.testing INFO
      info message
    pdblogger.testing WARNING
      warning message
    pdblogger.testing ERROR
      error message
    pdblogger.testing ERROR
      exception message: Forced program exception
    pdblogger.testing CRITICAL
      critical message
    >>> testing_handler.clear()

The handler can also be configured to log records that do *not* match
the expression.

    >>> handler.removeFilter(re_filter)
    >>> re_filter = pdblogger.ReFilter(
    ...     'Forced program exception', matched=False)
    >>> handler.addFilter(re_filter)

    >>> testing.main()
    TESTING pdb.set_trace() called: (<pdb.Pdb instance at 0x...>, <frame object at 0x...>), {}
    TESTING pdb.set_trace() called: (<pdb.Pdb instance at 0x...>, <frame object at 0x...>), {}
    >>> print testing_handler
    pdblogger.testing DEBUG
      debug message
    pdblogger.testing INFO
      info message
    pdblogger.testing WARNING
      warning message
    pdblogger.testing ERROR
      error message
    pdblogger.testing ERROR
      exception message: Forced program exception
    pdblogger.testing CRITICAL
      critical message
    >>> testing_handler.clear()

The filter can also be configured to match against any combination of
the file and line number of the frame that logged the message.

    >>> TODO
