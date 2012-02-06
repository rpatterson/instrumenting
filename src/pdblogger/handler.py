import sys
import logging
import bdb
import pdb

marker = object()


class PdbHandler(logging.Handler):
    """Python logging handler for invoking pdb on logging events."""

    logger = logging.getLogger('pdblogger')

    post_mortem = True

    def __init__(self, level=logging.ERROR, post_mortem=marker):
        super(PdbHandler, self).__init__(level=level)
        if post_mortem is not marker:
            self.post_mortem = post_mortem
        self.pdb = pdb.Pdb()

    def emit(self, record):
        self.pdb.reset()
        if self.post_mortem and record.exc_info:
            try:
                self.pdb.interaction(None, record.exc_info[2])
            except (bdb.BdbQuit, KeyboardInterrupt):
                pass
            except BaseException:
                disable_recursion = logging.Filter('pdblogger.recurse')
                self.addFilter(disable_recursion)
                try:
                    self.logger.exception('Exception while debugging')
                finally:
                    self.removeFilter(disable_recursion)
        else:
            frame = sys._getframe(6)
            try:
                self.pdb.set_trace(frame)
            except (bdb.BdbQuit, KeyboardInterrupt):
                pass
            except BaseException:
                disable_recursion = logging.Filter('pdblogger.recurse')
                self.addFilter(disable_recursion)
                try:
                    self.logger.exception('Exception while debugging')
                finally:
                    self.removeFilter(disable_recursion)
    
