import sys
import logging
import bdb
import pdb

from instrumenting import utils


class PdbHandler(utils.InstrumentingHandler):
    """Python logging handler for invoking pdb on logging events."""

    def __init__(self, level=logging.ERROR, post_mortem=True):
        utils.InstrumentingHandler.__init__(self, level=level)
        self.post_mortem = post_mortem
        self.pdb = pdb.Pdb()

    def emit(self, record):
        for attr in ('stdin', 'stdout'):
            tty = getattr(self.pdb, attr)
            if not (hasattr(tty, 'isatty')
                    and tty.isatty()):
                self.log(
                    logging.ERROR,
                    'Not invoking pdb, %s is not a tty: %s'
                    % (attr, getattr(tty, 'name', tty)))
                return
        
        self.pdb.reset()
        kw = {}
        if self.post_mortem and record.exc_info:
            func = self.pdb.interaction
            args = (None, record.exc_info[2])
        else:
            frame = sys._getframe(6)
            func = self.pdb.set_trace
            args = (frame, )

        try:
            func(*args, **kw)
        except (bdb.BdbQuit, KeyboardInterrupt):
            pass
        except BaseException:
            self.log(logging.ERROR, 'Exception while debugging',
                     exc_info=sys.exc_info())
        
