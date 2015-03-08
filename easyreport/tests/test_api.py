from unittest import TestCase
from nose.tools import assert_raises
import os
import sys



cpath = os.path.dirname(os.path.realpath(__file__)) + os.sep + '..' + os.sep + '..'
sys.path.insert(0,cpath)

from easyreport import EasyReport, Feature
import tempfile

class TestAPIWriter(TestCase):

    def setUp(self):
        self.file = tempfile.mktemp()
        self.yml = self.file + '.yml'

    def test_init(self):
        # invalid init
        try:
            R = EasyReport()
            error_thrown = False
        except:
            error_thrown = True
        self.assertTrue(error_thrown)

        # init
        R = EasyReport(file=self.file)
        self.assertEqual(R.file, self.yml)
        self.assertTrue(hasattr(R, 'sections'))

    def test_section(self):
        R = EasyReport(file=self.file)
        try:
            R.add('models', 1)   # provide an invalid value
            error_thrown = False
        except:
            error_thrown = True
        self.assertTrue(error_thrown)

        F = Feature(self.yml)
        R.add('models', (1,2))  # add a tuple as test
        R.add('models', F)  # add feature
        R.add('observations', (3,4))
        R.add('misc', (5,6))

        self.assertEqual(len(R.sections.keys()),3)
        for k in R.sections.keys():
            self.assertTrue(k in ['models', 'observations', 'misc'])

        self.assertEqual(len(R.sections['models']), 2)
        self.assertEqual(len(R.sections['observations']), 1)
        self.assertEqual(len(R.sections['misc']), 1)

        self.assertEqual(R.sections['models'][0][1], 2)
        self.assertEqual(R.sections['observations'][0][3], 4)
        self.assertEqual(R.sections['misc'][0][5], 6)

    def test_save(self):
        R = EasyReport(file=self.file)
        R.save()
        self.assertTrue(os.path.exists(self.yml))


class TestFeature(TestCase):

    def setUp(self):
        self.file = tempfile.mktemp()
        self.yml = self.file + '.yml'

