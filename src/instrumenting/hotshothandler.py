import hotshot

from instrumenting import profilehandler


class HotshotHandler(profilehandler.BaseProfilingHandler):
    """Use the experimental `hotshot` module to profile on logging events."""

    def setUpProfiler(self):
        self.profiler = hotshot.Profile()
        self.enable = self.profiler.start
        self.disable = self.profiler.stop

    def get_stats(self, stream):
        raise NotImplemented
