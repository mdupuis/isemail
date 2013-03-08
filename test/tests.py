#!/usr/bin/env python
#
# Test suite for isemail.py
#
# This suite actually just loads the XML-based test suite used by isemail.php.

from __future__ import print_function, unicode_literals


import errno
import glob
import os
import unittest


def load_xml_tests(filename):
    """Returns a TestSuite for the XML-drives tests in `filename`."""
    suite = unittest.TestSuite()
    raise NotImplementedError("Can't load {0}".format(filename))
    return suite


def load_tests(loader, tests, pattern):
    """
    Returns the tests to run based on the XML-driven test suite.

    Follows the load_tests protocol:
    http://docs.python.org/2/library/unittest.html#load-tests-protocol
    """
    dirname = os.path.dirname(__file__)
    for filename in sorted(glob.glob(os.path.join(dirname, 'tests*.xml'))):
        try:
            loaded = load_xml_tests(filename=filename)
        except IOError as e:
            if e.errno == errno.ENOENT:
                continue        # We must have raced against remove.
            raise
        else:
            tests.addTests(tests=loaded)
    return tests


if __name__ == '__main__':
    unittest.main()
