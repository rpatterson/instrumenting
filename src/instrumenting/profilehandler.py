import sys
import logging
import profile
import pstats

try:
    import cStringIO as StringIO
    StringIO  # pyflakes
except ImportError:
    import StringIO

from instrumenting import utils


class BaseProfilingHandler(utils.InstrumentingHandler):
    """
    Python logging handler which profiles code.

    It can also optionally log profiling stats and/or dump the raw
    stats to a file.
    """

    def __init__(self, start=False, stop=False, functions=None,
                 restriction=[50], strip_dirs=True, 
                 sort_stats=['cumulative'], print_formats=['stats'],
                 level=logging.NOTSET):
        utils.InstrumentingHandler.__init__(self, level=level)
        self.setUpProfiler()
        self.start = start
        self.stop = stop
        self.functions = functions
        self.print_formats = print_formats

    def emit(self, record):
        """
        Start or stop the configured profiler logging details.

        If the handler is configured to start the profiler and it is
        already started, a warning message is logged and it is left
        running.  Similarly, if the handler is configured to stop the
        profiler and it is already stopped, a warning message is
        logged and it is not started.

        In order to avoid surprising performance impacts, if the
        handler is configured such that it enables and disables the
        profiler for the same single log message, an error message is
        logged but the profiler is still disabled.
        """
        started = False

        if self.start:
            if self.running():
                self.log(logging.WARNING,
                         'Profiler %r already running, ignoring start'
                         % self.profiler)
            else:
                self.log(logging.INFO,
                         'Starting profiler %r' % self.profiler)
                import pdb; pdb.set_trace()
                self.enable()
                started = True

        if self.stop:
            if not self.running():
                self.log(logging.WARNING,
                         'Profiler %r not running, ignoring stop'
                         % self.profiler)
            else:
                if started:
                    self.log(logging.ERROR,
                             'Handler for profiler %r configured to start '
                             'and stop for the same log message'
                             % self.profiler)
                self.log(logging.INFO,
                         'Stopping profiler %r' % self.profiler)
                import pdb; pdb.set_trace()
                self.disable()

                if not started and self.print_formats:
                    self.log(logging.DEBUG, 'Printing profiler %r stats:\n%s'
                             % (self.profiler, self.log_stats()))

    def log_stats(self):
        stream = StringIO.StringIO()
        stats = self.get_stats(stream)
        if stats is None:
            return

        if self.strip_dirs:
            stats.strip_dirs()
        if self.sort_stats:
            stats.sort_stats(self.sort_stats)
        for method in self.print_formats:
            getattr(stats, 'print_'+method)(*self.restriction)
        return stream.getvalues()

    # Profiler specific support

    def setUpProfiler(self):
        """Set up the selected profiler."""
        raise NotImplemented

    def enable(self):
        raise NotImplemented

    def disable(self):
        raise NotImplemented

    def running(self):
        return isinstance(sys.getprofile(), type(self.profiler))

    def get_stats(self, stream):
        if self.running():
            self.log(logging.ERROR,
                     "Cannot get stats when the profiler from the "
                     "`profile` module is already running")
            return None
        import pdb; pdb.set_trace()
        stats = pstats.Stats(self.profiler, stream=stream)
        return stats


class ProfileHandler(BaseProfilingHandler):
    """Use the pure-python `profile` module to profile on logging events."""

    def setUpProfiler(self):
        if not self.functions:
            raise ValueError(
                'The `profile` module does not support profiling '
                'an already running stack')
        self.profiler = profile.Profile()

    def running(self):
        hook = sys.getprofile()
        return (hook is self.profiler.dispatcher
                and isinstance(hook.im_self, type(self.profiler)))
