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
from xml.etree import ElementTree


class IsEmailTestCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(IsEmailTestCase, self).__init__(*args, **kwargs)
        self._ready = False

    @classmethod
    def create(cls, filename, test_id, address,
               comment, category, diagnosis, source, sourcelink):
        obj = cls('run_test')
        obj._ready = True
        obj.filename = filename
        obj.test_id = test_id
        obj.address = address
        obj.comment = comment
        obj.category = category
        obj.diagnosis = diagnosis
        obj.source = source
        obj.sourcelink = sourcelink
        return obj

    def id(self):
        return '{filename} #{test_id}'.format(filename=self.filename,
                                              test_id=self.test_id)

    def __unicode__(self):
        return '{address} ({location})'.format(address=self.address,
                                               location=self.id())

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __repr__(self):
        return str(self)

    def run_test(self):
        self.assertEqual(
            'isemail({0!r})'.format(self.address),  # TODO: Use real function
            self.diagnosis
        )


def load_isemail_tests(filename):
    """Returns a TestSuite for the XML-drives tests in `filename`."""
    suite = unittest.TestSuite()
    root = ElementTree.parse(filename).getroot()
    for test in root.iter('test'):
        case = IsEmailTestCase.create(filename=filename,
                                      test_id=int(test.get('id')),
                                      address=test.findtext('address'),
                                      comment=test.findtext('comment'),
                                      category=test.findtext('category'),
                                      diagnosis=test.findtext('diagnosis'),
                                      source=test.findtext('source'),
                                      sourcelink=test.findtext('sourcelink'))
        suite.addTest(case)
        print(case)
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
            loaded = load_isemail_tests(filename=filename)
        except IOError as e:
            if e.errno == errno.ENOENT:
                continue        # We must have raced against remove.
            raise
        else:
            tests.addTests(tests=loaded)
    return tests


if __name__ == '__main__':
    unittest.main()
