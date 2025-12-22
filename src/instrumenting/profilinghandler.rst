.. -*-doctest-*-

========================
Profiler Logging Handler
========================

Start with a multi-threaded Python program we want to profile with
``profile``.

    >>> from instrumenting import testing
    >>> testing.threaded_main
    <function threaded_main at 0x...>

To begin there is no profiling data.

    >>> import os
    >>> 'instrumenting.prof' in os.listdir(tmp)
    False

Before a profiling handler is configued, logging events are just
printed to stderr.  The program logs messages at all logging levels
and also logs an exception.

    >>> testing.threaded_main()
    >>> print(testing_handler)
    instrumenting.testing DEBUG
      debug message
    instrumenting.testing INFO
      info message
    instrumenting.testing INFO
      other thread info message
    instrumenting.testing WARNING
      warning message
    instrumenting.testing WARNING
      other thread warning message
    instrumenting.testing ERROR
      error message
    instrumenting.testing ERROR
      other thread error message
    instrumenting.testing ERROR
      exception message: Forced program exception
    instrumenting.testing CRITICAL
      critical message
    >>> testing_handler.clear()

Since the profiling handler is best suited for starting and stopping
profiling on very specific logging messages it's not generally useful
to control which log messages start or stop profiling using `logging`
levels.  For that reason, the logging handlers default level is
`logging.NOTSET` so that it will match any log message.  The more
common usage will be to add a `instrumenting.ReFilter` to the
profiling handler to control when it starts or stops profiling.
    
Install a profiling handler that starts profiling and another handler
that stops profiling.

    >>> import logging
    >>> import instrumenting
    >>> root = logging.getLogger()

    >>> start = instrumenting.ProfilingHandler(start=True)
    >>> re_filter = instrumenting.ReFilter(
    ...     '^(debug|info|warning) message$', operation='match')
    >>> start.addFilter(re_filter)
    >>> root.addHandler(start)

    >>> stop = instrumenting.ProfilingHandler(level=logging.ERROR, stop=True)
    >>> root.addHandler(stop)

The default profiler is cProfile.

    >>> start.profiler
    <cProfile.Profile object at 0x...>

Now the program still prints messages to stderr but also collects
profiling data on all code execution within the thread that logged the
message under the specified function.  Other than that, execution
continues as it did before.  Note that the logging is configured in
the main thread but takes effect in child threads.

    >>> testing.threaded_main()
    >>> print(testing_handler)
    instrumenting.testing DEBUG
      debug message
    instrumenting INFO
      Starting profiler 'cProfile'
    instrumenting.testing INFO
      info message
    instrumenting WARNING
      Profiler 'cProfile' already running, ignoring start
    instrumenting.testing INFO
      other thread info message
    instrumenting.testing WARNING
      warning message
    instrumenting WARNING
      Profiler 'cProfile' already running, ignoring start
    instrumenting.testing WARNING
      other thread warning message
    instrumenting.testing ERROR
      error message
    instrumenting INFO
      Stopping profiler 'cProfile'
    instrumenting.testing ERROR
      other thread error message
    instrumenting WARNING
      Profiler 'cProfile' not running, ignoring stop
    instrumenting.testing ERROR
      exception message: Forced program exception
    instrumenting WARNING
      Profiler 'cProfile' not running, ignoring stop
    instrumenting.testing CRITICAL
      critical message
    instrumenting WARNING
      Profiler 'cProfile' not running, ignoring stop
    >>> testing_handler.clear()

The profiling data is written to a `instrumenting.prof` file by
default.

    >>> os.listdir(tmp)
    ...
    instrumenting.prof
    ...
    >>> pos = open('instrumenting.prof').tell()

The thread that doesn't log any matched messages is ???NOT??? profiled.

    >>> import re
    >>> import StringIO
    >>> import pstats
    >>> stream = StringIO.StringIO()
    >>> stats = pstats.Stats('instrumenting.prof', stream=stream)
    >>> printed = stream.getvalue()
    >>> 'instrumenting_testing_main' in printed
    True
    >>> 'threaded_inner_unprofiled' in printed
    False

If we remove the filter that excluded the other thread, then both
threads are profiled.

    >>> start.removeFilter(re_filter)

    >>> testing.threaded_main()
    TESTING started profiling: (TODO,), {}
    TESTING already profiling: (TODO,), {}
    TESTING started profiling: (TODO,), {}
    TESTING already profiling: (TODO,), {}
    TESTING already profiling: (TODO,), {}
    TESTING already profiling: (TODO,), {}
    TESTING stopped profiling: (TODO,), {}
    TESTING stopped profiling: (TODO,), {}
    TESTING not profiling: (TODO,), {}
    TESTING not profiling: (TODO,), {}
    >>> print(testing_handler)
    instrumenting.testing DEBUG
      debug message
    instrumenting.testing INFO
      info message
    instrumenting.testing INFO
      other thread info message
    instrumenting.testing WARNING
      warning message
    instrumenting.testing WARNING
      other thread warning message
    instrumenting.testing ERROR
      error message
    instrumenting.testing ERROR
      other thread error message
    instrumenting.testing ERROR
      exception message: Forced program exception
    instrumenting.testing CRITICAL
      critical message
    >>> testing_handler.clear()

Also, the profiling data file is appended to rather than being
overwritten.  Truncate the file to clear profiling data.  Depending on
the application, this may require stopping the application.

    >>> pos < open('instrumenting.prof').tell()
    True

The path to the profiling data file can be specified allowing
profiling of multiple execution paths separately.

    >>> root.removeHandler(start)
    >>> start = instrumenting.ProfilingHandler(
    ...     start=True, filename='instrumenting-testing.prof')
    >>> root.addHandler(start)

    >>> testing.threaded_main()
    TESTING started profiling: (TODO,), {}
    TESTING already profiling: (TODO,), {}
    TESTING started profiling: (TODO,), {}
    TESTING already profiling: (TODO,), {}
    TESTING already profiling: (TODO,), {}
    TESTING already profiling: (TODO,), {}
    TESTING stopped profiling: (TODO,), {}
    TESTING stopped profiling: (TODO,), {}
    TESTING not profiling: (TODO,), {}
    TESTING not profiling: (TODO,), {}
    >>> print(testing_handler)
    instrumenting.testing DEBUG
      debug message
    instrumenting.testing INFO
      info message
    instrumenting.testing INFO
      other thread info message
    instrumenting.testing WARNING
      warning message
    instrumenting.testing WARNING
      other thread warning message
    instrumenting.testing ERROR
      error message
    instrumenting.testing ERROR
      other thread error message
    instrumenting.testing ERROR
      exception message: Forced program exception
    instrumenting.testing CRITICAL
      critical message
    >>> testing_handler.clear()

    >>> os.listdir(tmp)
    ...
    instrumenting.prof
    ...
    >>> pos = open('instrumenting.prof').tell()
