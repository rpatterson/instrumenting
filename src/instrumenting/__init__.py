"""Tools for instrumenting Python code using logging."""

from instrumenting.filter import ReFilter

from instrumenting.pdbhandler import PdbHandler

from instrumenting.profilehandler import ProfileHandler
try:
    from instrumenting.cprofilehandler import CProfileHandler
    ProfilingHandler = CProfileHandler
except ImportError:
    ProfilingHandler = ProfileHandler
try:
    from instrumenting.hotshothandler import HotshotHandler
except ImportError:
    pass
