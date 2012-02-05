.. -*-doctest-*-

=========
PdbLogger
=========

Start with a Python program we want to debug with ``pdb``.

    >>> from pdbhandler import testing
    >>> testing.main
    <function main at 0x...>

For testing ``set_trace()`` and ``post_mortem`` both just log a
message.

    >>> import pdb
    >>> pdb.set_trace()
    DEBUG pdbhandler.testing pdb.set_trace() called
    >>> pdb.post_mortem()
    DEBUG pdbhandler.testing pdb.post_mortem() called

Before a pdb logging handler is configued, logging events are just
printed to stderr.  The program logs messages at all logging levels
and also logs an exception.

    >>> testing.main()
    DEBUG pdbhandler.testing debug message
    INFO pdbhandler.testing info message
    WARNING pdbhandler.testing warning message
    ERROR pdbhandler.testing error message
    ERROR pdbhandler.testing exception message
    CRITICAL pdbhandler.testing critical message
    
Configure a pdb logging handler that does post_mortem debugging of
exceptions.

    >>> import logging
    >>> import pdbhandler
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
    DEBUG pdbhandler.testing debug message
    INFO pdbhandler.testing info message
    WARNING pdbhandler.testing warning message
    ERROR pdbhandler.testing error message
    DEBUG pdbhandler.testing pdb.set_trace() called
    ERROR pdbhandler.testing exception message
    DEBUG pdbhandler.testing pdb.post_mortem() called
    CRITICAL pdbhandler.testing critical message

Whether to use ``set_trace()`` or ``post_mortem()`` can also be
configured manually when instantiating the logger.

    >>> root.removeLogger(handler)
    >>> handler = pdblogger.PdbHandler(post_mortem=False)
    >>> root.addHandler(handler)

    >>> testing.main()
    DEBUG pdbhandler.testing debug message
    INFO pdbhandler.testing info message
    WARNING pdbhandler.testing warning message
    ERROR pdbhandler.testing error message
    DEBUG pdbhandler.testing pdb.set_trace() called
    ERROR pdbhandler.testing exception message
    DEBUG pdbhandler.testing pdb.set_trace() called
    CRITICAL pdbhandler.testing critical message


Error Handling
==============

If ``pdb`` is exited either by the ``quit`` debugger command or via a
keyboard interrupt (``Ctrl-C``), the program execution also continues
as it did before.

    >>> root.removeLogger(handler)
    >>> handler = pdblogger.PdbHandler()
    >>> root.addHandler(handler)

    >>> pdb.set_trace = testing.quitting_set_trace
    >>> pdb.set_trace()
    Traceback (most recent call last):
    BdbQuit
    >>> pdb.post_mortem = testing.quitting_post_mortem
    >>> pdb.post_mortem()
    Traceback (most recent call last):
    BdbQuit

    >>> testing.main()
    DEBUG pdbhandler.testing debug message
    INFO pdbhandler.testing info message
    WARNING pdbhandler.testing warning message
    ERROR pdbhandler.testing error message
    DEBUG pdbhandler.testing pdb.set_trace() called
    ERROR pdbhandler.testing exception message
    DEBUG pdbhandler.testing pdb.post_mortem() called
    CRITICAL pdbhandler.testing critical message

    >>> pdb.set_trace = testing.interrupting_set_trace
    >>> pdb.set_trace()
    Traceback (most recent call last):
    KeyboardInterrupt
    >>> pdb.post_mortem = testing.interrupting_post_mortem
    >>> pdb.post_mortem()
    Traceback (most recent call last):
    KeyboardInterrupt

    >>> testing.main()
    DEBUG pdbhandler.testing debug message
    INFO pdbhandler.testing info message
    WARNING pdbhandler.testing warning message
    ERROR pdbhandler.testing error message
    DEBUG pdbhandler.testing pdb.set_trace() called
    ERROR pdbhandler.testing exception message
    DEBUG pdbhandler.testing pdb.post_mortem() called
    CRITICAL pdbhandler.testing critical message

If invoking ``pdb`` or anything done in the debugger raises another
error which causes the debugger to exit, details are logged but
program execution also continues as it did before.

    >>> pdb.set_trace = testing.excepting_set_trace
    >>> pdb.set_trace()
    Traceback (most recent call last):
    ValueError: pdbhandler.testing set_trace forced exception
    >>> pdb.post_mortem = testing.excepting_post_mortem
    >>> pdb.post_mortem()
    Traceback (most recent call last):
    ValueError: pdbhandler.testing post_mortem forced exception

    >>> testing.main()
    DEBUG pdbhandler.testing debug message
    INFO pdbhandler.testing info message
    WARNING pdbhandler.testing warning message
    ERROR pdbhandler.testing error message
    ERROR pdbhandler.testing Exception while debugging:
    Traceback (most recent call last):
    ValueError: pdbhandler.testing set_trace forced exception
    ERROR pdbhandler.testing exception message
    ERROR pdbhandler.testing Exception while debugging:
    Traceback (most recent call last):
    ValueError: pdbhandler.testing post_mortem forced exception
    CRITICAL pdbhandler.testing critical message

If ``stdin`` and ``stdout`` are not real terminals and thus can't be
used by the debugger, the pdb logging handler will not invoke ``pdb``:

    >>> import pdbhandler.handler
    >>> import tempfile
    >>> pdbhandler.handler.stdin = tempfile.TemporaryFile()

    >>> testing.main()
    DEBUG pdbhandler.testing debug message
    INFO pdbhandler.testing info message
    WARNING pdbhandler.testing warning message
    ERROR pdbhandler.testing error message
    DEBUG pdbhandler.testing not invoking set_trace, stdin is not a tty: .../tmp...
    ERROR pdbhandler.testing exception message
    DEBUG pdbhandler.testing not invoking post_mortem, stdin is not a tty: .../tmp...
    CRITICAL pdbhandler.testing critical message
