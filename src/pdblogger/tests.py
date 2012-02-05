import unittest
import doctest


def test_suite():
    return doctest.DocFileSuite(
        'tests.txt',
        optionflags=(doctest.ELLIPSIS|doctest.REPORT_NDIFF))
        
if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
