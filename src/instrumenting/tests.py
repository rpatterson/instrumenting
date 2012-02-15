import unittest
try:
    from zope.testing import doctest
    doctest  # pyflakes
except ImportError:
    import doctest

from instrumenting import testing


def test_suite():
    return doctest.DocFileSuite(
        'pdbhandler.rst',
        'filter.rst',
        setUp=testing.setUp, tearDown=testing.tearDown,
        optionflags=(doctest.ELLIPSIS|doctest.REPORT_NDIFF))
        
if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
