'''
Created on Mar 17, 2010

@author: jose
'''

import unittest
from cStringIO import StringIO

from cloudlight.classes.graph import Graph
from cloudlight.tests.data import example_txt2

class Test(unittest.TestCase):


    def setUp(self):
        self.graph = Graph()
        self.graph.debug = False
        self.graph.input_debug_links = 200000
        self.graph.output_debug_nodes = 10000
        self.graph.load_edgelist(StringIO(example_txt2))


    def tearDown(self):
        pass


    def testInternalScalingGrowth(self):
        self.assertEqual( list(self.graph.internal_scaling_growth('jcl5m')),
                          [1, 2, 22, 44])
        

    def testInternalScalingDimension(self):
        self.assertEqual( list(self.graph.internal_scaling_dimension('jcl5m')),
                          [-1.0, -1.0, 4.4594316186372973, 3.4445178457870527])
        

    def testConnectivityGrowth(self):
        self.assertEqual( list( self.graph.connectivity_growth('jcl5m') ),
                          [1, 21, 43, 0])
        

    def testConnectivityDimension(self):
        self.assertEqual( list(self.graph.connectivity_dimension('jcl5m')),
                          [-1.0, -1.0, 5.4262647547020979, -1.0])
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
