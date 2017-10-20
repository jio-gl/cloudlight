'''
Created on Apr 6, 2010

@author: jose
'''
import unittest

from cloudlight.classes.graph import Graph
from cloudlight.algorithms.plot import Plot
import cloudlight.tests.data_enc1


class PlotStressTest2(unittest.TestCase):


    def setUp(self):
        self.graph = Graph()
        self.graph.debug = False
        self.graph.input_debug_links = 50000
        self.graph.max_links_input = 25000
        self.graph.output_debug_nodes = 10000
        use_big_alphabet = False
        self.graph.load_compressed_graph(cloudlight.tests.data_enc1, use_big_alphabet)


    def tearDown(self):
        pass


    def testCompleteAnalysis(self):
        
        p = Plot()
        p.debug = False
        sample_size = 10
        bins = 10
        p.init_complete_analysis(self.graph, '/tmp/graph_analysis', sample_size, bins)
        p.complete_analysis(self.graph)
        #p.plot_graph_params()    



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()