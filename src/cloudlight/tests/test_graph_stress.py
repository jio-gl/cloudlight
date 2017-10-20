'''
Created on Mar 30, 2010

@author: jose
'''

import unittest
from cStringIO import StringIO

from cloudlight.classes.graph import Graph
import cloudlight.tests.data_enc1
import cloudlight.tests.data_enc2


class Test(unittest.TestCase):


    def setUp(self):
        self.graph = Graph()
        self.graph.debug = False
        self.graph.max_links_input = 100000
        self.graph.input_debug_links = 200000
        self.graph.output_debug_nodes = 10000
    

    def testLoadCompressed1(self):
        use_big_alphabet = False
        self.graph.load_compressed_graph(cloudlight.tests.data_enc1, use_big_alphabet)
        
        self.assertEqual( self.graph.number_of_nodes(), 43948 )
        self.assertEqual( self.graph.number_of_edges(), 50000 )


    def testLoadCompressed2(self):
        use_big_alphabet = True
        self.graph.load_compressed_graph(cloudlight.tests.data_enc2, use_big_alphabet)
        
        self.assertEqual( self.graph.number_of_nodes(), 43948 )
        self.assertEqual( self.graph.number_of_edges(), 50000 )


    def tearDown(self):
        pass


        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
