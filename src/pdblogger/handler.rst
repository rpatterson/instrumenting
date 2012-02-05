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
    DEBUG pdblogger.testing pdb.Pdb.set_trace() called
    >>> pdb.post_mortem()
    DEBUG pdblogger.testing pdb.Pdb.interaction() called

Before a pdb logging handler is configued, logging events are just
printed to stderr.  The program logs messages at all logging levels
and also logs an exception.

    >>> testing.main()
    DEBUG pdblogger.testing debug message
    INFO pdblogger.testing info message
    WARNING pdblogger.testing warning message
    ERROR pdblogger.testing error message
    ERROR pdblogger.testing exception message
    CRITICAL pdblogger.testing critical message
    
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
available and ``set_trace()`` if not.  After the debugger is exited
via the ``continue`` debuger command, the program execution continues
as it did before.

    >>> testing.main()
    DEBUG pdblogger.testing debug message
    INFO pdblogger.testing info message
    WARNING pdblogger.testing warning message
    ERROR pdblogger.testing error message
    DEBUG pdblogger.testing pdb.Pdb.set_trace() called
    ERROR pdblogger.testing exception message
    DEBUG pdblogger.testing pdb.Pdb.interaction() called
    CRITICAL pdblogger.testing critical message

Whether to use ``set_trace()`` or ``post_mortem()`` can also be
configured manually when instantiating the logger.

    >>> root.removeLogger(handler)
    >>> handler = pdblogger.PdbHandler(post_mortem=False)
    >>> root.addHandler(handler)

    >>> testing.main()
    DEBUG pdblogger.testing debug message
    INFO pdblogger.testing info message
    WARNING pdblogger.testing warning message
    ERROR pdblogger.testing error message
    DEBUG pdblogger.testing pdb.Pdb.set_trace() called
    ERROR pdblogger.testing exception message
    DEBUG pdblogger.testing pdb.Pdb.set_trace() called
    CRITICAL pdblogger.testing critical message


Error Handling
==============

If ``pdb`` is exited either by the ``quit`` debugger command or via a
keyboard interrupt (``Ctrl-C``), the program execution also continues
as it did before.

    >>> root.removeLogger(handler)
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
    DEBUG pdblogger.testing debug message
    INFO pdblogger.testing info message
    WARNING pdblogger.testing warning message
    ERROR pdblogger.testing error message
    DEBUG pdblogger.testing pdb.Pdb.set_trace() called
    ERROR pdblogger.testing exception message
    DEBUG pdblogger.testing pdb.Pdb.interaction() called
    CRITICAL pdblogger.testing critical message

    >>> pdb.Pdb.set_trace = testing.interrupting_set_trace
    >>> pdb.set_trace()
    Traceback (most recent call last):
    KeyboardInterrupt
    >>> pdb.Pdb.interaction = testing.interrupting_interaction
    >>> pdb.post_mortem()
    Traceback (most recent call last):
    KeyboardInterrupt

    >>> testing.main()
    DEBUG pdblogger.testing debug message
    INFO pdblogger.testing info message
    WARNING pdblogger.testing warning message
    ERROR pdblogger.testing error message
    DEBUG pdblogger.testing pdb.Pdb.set_trace() called
    ERROR pdblogger.testing exception message
    DEBUG pdblogger.testing pdb.Pdb.interaction() called
    CRITICAL pdblogger.testing critical message

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
    DEBUG pdblogger.testing debug message
    INFO pdblogger.testing info message
    WARNING pdblogger.testing warning message
    ERROR pdblogger.testing error message
    ERROR pdblogger.testing Exception while debugging:
    Traceback (most recent call last):
    ValueError: pdblogger.testing set_trace forced exception
    ERROR pdblogger.testing exception message
    ERROR pdblogger.testing Exception while debugging:
    Traceback (most recent call last):
    ValueError: pdblogger.testing interaction forced exception
    CRITICAL pdblogger.testing critical message

If ``stdin`` and ``stdout`` are not real terminals and thus can't be
used by the debugger, the pdb logging handler will not invoke ``pdb``:

    >>> import pdblogger.handler
    >>> import tempfile
    >>> pdblogger.handler.stdin = tempfile.TemporaryFile()

    >>> testing.main()
    DEBUG pdblogger.testing debug message
    INFO pdblogger.testing info message
    WARNING pdblogger.testing warning message
    ERROR pdblogger.testing error message
    DEBUG pdblogger.testing not invoking set_trace, stdin is not a tty: .../tmp...
    ERROR pdblogger.testing exception message
    DEBUG pdblogger.testing not invoking interaction, stdin is not a tty: .../tmp...
    CRITICAL pdblogger.testing critical message
