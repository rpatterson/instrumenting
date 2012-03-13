import unittest
try:
    from zope.testing import doctest
    doctest  # pyflakes
except ImportError:
    import doctest

from instrumenting import testing


def test_suite():
    return unittest.TestSuite([
        doctest.DocFileSuite(
            'pdbhandler.rst',
            'filter.rst',
            setUp=testing.setUpPdb, tearDown=testing.tearDownPdb,
            optionflags=(doctest.ELLIPSIS|doctest.REPORT_NDIFF)),
        doctest.DocFileSuite(
            'profilinghandler.rst',
            setUp=testing.setUpProfiling, tearDown=testing.tearDownProfiling,
            optionflags=(doctest.ELLIPSIS|doctest.REPORT_NDIFF))
        ])


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
