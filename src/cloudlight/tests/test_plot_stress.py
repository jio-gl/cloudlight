'''
Created on Apr 5, 2010

@author: jose
'''

import random
import unittest
from cStringIO import StringIO

from cloudlight.classes.graph import Graph
import cloudlight.tests.data_enc1
import cloudlight.tests.data_enc2
from cloudlight.algorithms.plot import Plot


class PlotStressTest(unittest.TestCase):


    def setUp(self):
        self.graph = Graph()
        self.graph.debug = False
        self.graph.input_debug_links = 500000
        self.graph.output_debug_nodes = 10000
        use_big_alphabet = False
        self.graph.load_compressed_graph(cloudlight.tests.data_enc1, use_big_alphabet)

        random.seed(666)
        self.nodes = self.graph.random_nodes(10000)


    def tearDown(self):
        pass


    def testDegree(self):       
         
        degrees = list(self.graph.degrees(self.nodes))        
        p = Plot()    
        p.clear()    
        p.title = 'Degree distribution'
        p.x_label = 'd : node degree'
        p.y_label = 'P(d)'
        p.dist_plot( degrees, 10, True, True, True )
        #p.show()
        pass


    def testClust(self):        
        clusts = list(self.graph.clustering_indices(self.nodes))
        p = Plot()    
        p.clear()    
        p.title = 'Clustering index distribution'
        p.x_label = 'c : node clustering index'
        p.y_label = 'P(c)'
        _, _ = p.dist_plot( clusts, 10, True, True, True )
        #p.show()
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()