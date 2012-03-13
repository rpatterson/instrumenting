import logging


class InstrumentingHandler(logging.Handler):

    logger = logging.getLogger('instrumenting')

    def __init__(self, *args, **kw):
        logging.Handler.__init__(self, *args, **kw)
        self.recursion_filter = logging.Filter('instrumenting.recursion')

    def log(self, level, msg, *args, **kw):
        self.addFilter(self.recursion_filter)
        try:
            self.logger.log(level, msg, *args, **kw)
        finally:
            self.removeFilter(self.recursion_filter)
