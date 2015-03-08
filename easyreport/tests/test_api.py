from unittest import TestCase
from nose.tools import assert_raises
import os
import sys



cpath = os.path.dirname(os.path.realpath(__file__)) + os.sep + '..' + os.sep + '..'
sys.path.insert(0,cpath)

from easyreport import EasyReport

class TestData(unittest.TestCase):

    def setUp(self):
        pass

    def test_init(self):



