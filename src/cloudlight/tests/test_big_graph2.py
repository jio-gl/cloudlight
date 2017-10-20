'''
Created on Apr 21, 2010

@author: jose
'''
import unittest
from cStringIO import StringIO

from cloudlight.classes.big_graph import BigGraph
from cloudlight.tests.data import example_txt2


class Test(unittest.TestCase):


    def setUp(self):
        
        self.graph = BigGraph()
        self.graph.debug = False
        self.graph.input_debug_links = 2*20 #200000
        self.graph.output_debug_nodes = 10000
        self.graph.load_edgelist(StringIO(example_txt2))

        self.graph.create_indices()

    def tearDown(self):
        pass


    def testName(self):
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()