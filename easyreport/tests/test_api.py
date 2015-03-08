from unittest import TestCase
from nose.tools import assert_raises
import os
import sys

cpath = os.path.dirname(os.path.realpath(__file__)) + os.sep
rpath =  cpath + '..' + os.sep + '..'
sys.path.insert(0, rpath)

from easyreport import EasyReport, Feature, GraphicFeature
import tempfile
import yaml

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

        F = Feature('a')
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
        # check saving of data to yml file
        R = EasyReport(file=self.file)
        R.add('models', (1,2))
        R.add('models', (3,4))
        R.add('observations', ('a','b'))
        R.save()
        self.assertTrue(os.path.exists(self.yml))

        x = yaml.load(open(self.yml))
        #1
        self.assertEqual(len(x.keys()),2)
        #2
        for k in x.keys():
            k in R.sections.keys()
        #3
        self.assertEqual(x['models'][0][1], 2)
        self.assertEqual(x['models'][1][3], 4)
        self.assertEqual(x['observations'][0]['a'], 'b')

        F = Feature('MPI-ESM', x=1, y=5, z='hello')



class TestFeature(TestCase):

    def setUp(self):
        pass

    def test_init(self):
        F = Feature('myid', a=1, b=5, c='hello')
        self.assertEqual(F.id, 'myid')
        self.assertEqual(F.a, 1)
        self.assertEqual(F.b, 5)
        self.assertEqual(F.c, 'hello')

    def test_graphic(self):
        G = GraphicFeature('theid', 'my caption', 'test.png', a=4, b=5, c='test')
        self.assertEqual(G.a, 4)
        self.assertEqual(G.id, 'theid')
        self.assertEqual(G.b, 5)
        self.assertEqual(G.c, 'test')
        self.assertEqual(G.caption, 'my caption')
        self.assertEqual(G.file, 'test.png')




