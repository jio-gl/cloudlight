'''
Created on Mar 19, 2010

@author: jose
'''

import unittest, random

from cloudlight.classes.graph import Graph
from cloudlight.algorithms.privacy_attack import PrivacyAttackStrategies
import cloudlight.tests.data_enc1


class PrivacyStressTest(unittest.TestCase):


    def setUp(self):

        self.graph = Graph()
        self.graph.debug = False
        self.graph.max_links_input = 100000
        self.graph.input_debug_links = 200000
        self.graph.output_debug_nodes = 10000
        use_big_alphabet = False
        self.graph.load_compressed_graph(cloudlight.tests.data_enc1, use_big_alphabet)
        self.graph.create_index_degree()
        self.graph.create_index_unseen_degree()

        lookahead = 0
        coverage = 'link'

        self.strategies = PrivacyAttackStrategies(self.graph, lookahead, coverage, False)
        
        random.seed(666)

        self.coverages = [0.1] # [ float(f)/100 for f in range(2, 104, 2) ]

    def testStrategyRandom(self):
                
        self.assertEqual( list(self.strategies.start_random([0.01]))[0], 117)
        

    def testStrategyDegree(self):
        
        self.assertEqual( list(self.strategies.start_degree(self.coverages))[0], 5)
        

    def testStrategyGreedy(self):
        
        self.assertEqual( list(self.strategies.start_greedy(self.coverages))[0], 5)
        

    def testStrategyCrawler(self):
        
        self.assertEqual( list(self.strategies.start_crawler(self.coverages))[0], 11)






if __name__ == "__main__":
    import sys;sys.argv = ['', 'Test.testName']
    unittest.main()