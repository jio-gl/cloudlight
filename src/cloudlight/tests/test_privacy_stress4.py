'''
Created on May 11, 2010

@author: jose
'''

import unittest, random

from cloudlight.classes.graph import Graph
from cloudlight.algorithms.privacy_attack import PrivacyAttackStrategies
import cloudlight.tests.data_enc1


class BigPrivacyStressTest4(unittest.TestCase):


    def setUp(self):
        self.graph = Graph()
        self.graph.debug = False
        self.graph.max_links_input = 5000
        self.graph.input_debug_links = 200000
        self.graph.output_debug_nodes = 10000
        use_big_alphabet = False
        self.graph.load_compressed_graph(cloudlight.tests.data_enc1, use_big_alphabet)
        self.graph.create_index_degree()
        self.graph.create_index_unseen_degree()

        lookahead = 1
        coverage = 'korolova node'

        self.strategies = PrivacyAttackStrategies(self.graph, lookahead, coverage, False)
        
        
        self.coverages = [0.8] # [ float(f)/100 for f in range(2, 104, 2) ]

    def testStrategyRandom(self):
        
        random.seed(6661)
                
        self.assertEqual( list(self.strategies.start_random([0.01]))[0], 1)
        

    def testStrategyDegree(self):
        
        random.seed(6662)
        
        self.assertEqual( list(self.strategies.start_degree(self.coverages))[0], 3)
        

    def testStrategyGreedy(self):

        random.seed(6663)
        
        self.assertEqual( list(self.strategies.start_greedy(self.coverages))[0], 3)
        

    def testStrategyCrawler(self):
        
        random.seed(6664)
        
        self.assertEqual( list(self.strategies.start_crawler(self.coverages))[0], 3)
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()