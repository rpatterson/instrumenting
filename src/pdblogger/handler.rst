.. -*-doctest-*-

=========
PdbLogger
=========

Start with a Python program we want to debug with ``pdb``.

    >>> from pdblogger import testing
    >>> testing.main
    <function main at 0x...>

For testing ``set_trace()`` and ``post_mortem`` both just log a
message.

    >>> import pdb
    >>> pdb.set_trace()
    TESTING pdb.set_trace() called: (<zope.testing.doctest._OutputRedirectingPdb instance at 0x...>,), {}
    >>> try:
    ...     raise ValueError('Forced testing exception')
    ... except:
    ...     pdb.post_mortem()
    TESTING pdb.interaction() called: (<pdb.Pdb instance at 0x...>, None, <traceback object at 0x...>), {}

Before a pdb logging handler is configued, logging events are just
printed to stderr.  The program logs messages at all logging levels
and also logs an exception.

    >>> testing.main()
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
    
Configure a pdb logging handler that does post_mortem debugging of
exceptions.

    >>> import logging
    >>> import pdblogger
    >>> root = logging.getLogger()
    >>> handler = pdblogger.PdbHandler()
    >>> root.addHandler(handler)

Now the program still prints messages to stderr but also invokes
``pdb`` for ``post_mortem`` debugging of the exception.  By default,
the handler will use ``post_mortem()`` if exception information is
available and ``set_trace()`` if not.  The handler also defaults to
the ``ERROR`` logging level.  After the debugger is exited via the
``continue`` debuger command, the program execution continues as it
did before.

    >>> testing.main()
    TESTING pdb.set_trace() called: (<pdb.Pdb instance at 0x...>, <frame object at 0x...>), {}
    TESTING pdb.interaction() called: (<pdb.Pdb instance at 0x...>, None, <traceback object at 0x...>), {}
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

Whether to use ``set_trace()`` or ``post_mortem()`` can also be
configured manually when instantiating the logger.

    >>> root.removeHandler(handler)
    >>> handler = pdblogger.PdbHandler(post_mortem=False)
    >>> root.addHandler(handler)

    >>> testing.main()
    TESTING pdb.set_trace() called: (<pdb.Pdb instance at 0x...>, <frame object at 0x...>), {}
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


Error Handling
==============

If ``pdb`` is exited either by the ``quit`` debugger command or via a
keyboard interrupt (``Ctrl-C``), the program execution also continues
as it did before.

    >>> root.removeHandler(handler)
    >>> handler = pdblogger.PdbHandler()
    >>> root.addHandler(handler)

    >>> pdb.Pdb.set_trace = testing.quitting_set_trace
    >>> pdb.set_trace()
    Traceback (most recent call last):
    BdbQuit
    >>> pdb.Pdb.interaction = testing.quitting_interaction
    >>> pdb.post_mortem()
    Traceback (most recent call last):
    BdbQuit

    >>> testing.main()
    TESTING pdb.set_trace() called: (<pdb.Pdb instance at 0x...>, <frame object at 0x...>), {}
    TESTING pdb.interaction() called: (<pdb.Pdb instance at 0x...>, None, <traceback object at 0x...>), {}
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

    >>> pdb.Pdb.set_trace = testing.interrupting_set_trace
    >>> try:
    ...     pdb.set_trace()
    ... except KeyboardInterrupt:
    ...     print 'TESTING interrupted'
    TESTING pdb.set_trace() called: (<zope.testing.doctest._OutputRedirectingPdb instance at 0x...>,), {}
    TESTING interrupted
    
    >>> pdb.Pdb.interaction = testing.interrupting_interaction
    >>> try:
    ...     pdb.post_mortem()
    ... except KeyboardInterrupt:
    ...     print 'TESTING interrupted'
    TESTING pdb.interaction() called: (<pdb.Pdb instance at 0x...>, None, <traceback object at 0x...>), {}
    TESTING interrupted

    >>> testing.main()
    TESTING pdb.set_trace() called: (<pdb.Pdb instance at 0x...>, <frame object at 0x...>), {}
    TESTING pdb.interaction() called: (<pdb.Pdb instance at 0x...>, None, <traceback object at 0x...>), {}
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

If invoking ``pdb`` or anything done in the debugger raises another
error which causes the debugger to exit, details are logged but
program execution also continues as it did before.

    >>> pdb.Pdb.set_trace = testing.excepting_set_trace
    >>> pdb.set_trace()
    Traceback (most recent call last):
    ValueError: pdblogger.testing set_trace forced exception
    >>> pdb.Pdb.interaction = testing.excepting_interaction
    >>> pdb.post_mortem()
    Traceback (most recent call last):
    ValueError: pdblogger.testing interaction forced exception

    >>> testing.main()
    TESTING pdb.set_trace() called: (<pdb.Pdb instance at 0x...>, <frame object at 0x...>), {}
    TESTING pdb.interaction() called: (<pdb.Pdb instance at 0x...>, None, <traceback object at 0x...>), {}
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
    pdblogger ERROR
      Exception while debugging
    pdblogger.testing ERROR
      exception message: Forced program exception
    pdblogger ERROR
      Exception while debugging
    pdblogger.testing CRITICAL
      critical message
    pdblogger ERROR
      Exception while debugging
    >>> testing_handler.clear()

If ``stdin`` and ``stdout`` are not real terminals and thus can't be
used by the debugger, the pdb logging handler will not invoke ``pdb``:

    >>> import pdblogger.handler
    >>> import tempfile
    >>> pdblogger.handler.stdin = tempfile.TemporaryFile()

    >>> testing.main()
    >>> print testing_handler
    pdblogger.testing DEBUG
      debug message
    pdblogger.testing INFO
      info message
    pdblogger.testing WARNING
      warning message
    pdblogger.testing ERROR
      error message
    pdblogger.testing DEBUG
      not invoking set_trace, stdin is not a tty: .../tmp...
    pdblogger.testing ERROR
      exception message: Forced program exception
    pdblogger.testing DEBUG
      not invoking interaction, stdin is not a tty: .../tmp...
    pdblogger.testing CRITICAL
      critical message
    >>> testing_handler.clear()
