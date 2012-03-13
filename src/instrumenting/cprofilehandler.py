import cProfile

from instrumenting import profilehandler


class CProfileHandler(profilehandler.BaseProfilingHandler):
    """Use the optimized `cProfile` module to profile on logging events."""

    def setUpProfiler(self):
        self.profiler = cProfile.Profile()
        self.enable = self.profiler.enable
        self.disable = self.profiler.disable
