=============
instrumenting
=============

This module provides logging handlers and filters for Python's logging
module can be used to instrument python code where that code logs
messages.  For example, the ``instrumenting.PdbHandler`` will invoke
pdb, the Python debugger, on logging events as configured.
