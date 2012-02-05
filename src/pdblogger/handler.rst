.. -*-doctest-*-

=========
PdbLogger
=========

Start with a Python program we want to debug with ``pdb``.

    >>> TODO

For testing ``set_trace()`` and ``post_mortem`` both just log a
message.

    >>> TODO

Before a pdb logging handler is configued, logging events are just
printed to stderr.  The program logs messages at all logging levels
and also logs an exception.

    >>> TODO

Configure a pdb logging handler that does post_mortem debugging of
exceptions.

    >>> TODO

Now the program still prints messages to stderr but also invokes
``pdb`` for ``post_mortem`` debugging of the exception.  By default,
the handler will use ``post_mortem()`` if exception information is
available.  After the debugger is exited via the ``continue`` debuger
command, the program execution continues as it did before.

    >>> TODO

If the handler is configured to handle events that have no exception
information, then ``set_trace()`` is used instead of ``post_mortem``.

    >>> TODO

Whether to use ``set_trace()`` or ``post_mortem()`` can also be
configured manually when instantiating the logger.

    >>> TODO force using set_trace for an exception


Error Handling
==============

If ``pdb`` is exited either by the ``quit`` debugger command or via a
keyboard interrupt (``Ctrl-C``), the program execution also continues
as it did before.

    >>> TODO

If invoking ``pdb`` or anything done in the debugger raises another
error which causes the debugger to exit, details are logged but
program execution also continues as it did before.

    >>> TODO

If ``stdin`` and ``stdout`` are not real terminals and thus can't be
used by the debugger, the pdb logging handler will not invoke ``pdb``:

    >>> TODO

