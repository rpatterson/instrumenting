import re
import logging

marker = object()


class ReFilter(logging.Filter):
    """Filter records that match or don't match a regular expression."""

    def __init__(self, pattern, matched=True, format="%(message)s",
                 operation='search', flags=0):
        self.pattern = re.compile(pattern, flags)
        self.check = getattr(self.pattern, operation)
        self.matched = matched
        self.format = format
        
    def filter(self, record):
        kw = record.__dict__.copy()
        kw['message'] = record.getMessage()
        string = self.format % kw
        match = self.check(string)
        if match is None:
            return int(not self.matched)
        else:
            return int(self.matched)
