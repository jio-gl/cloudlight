'''
Created on May 10, 2010

@author: jose
'''

import unittest, random

from cloudlight.classes.big_graph import BigGraph
from cloudlight.algorithms.privacy_attack import PrivacyAttackStrategies
import cloudlight.tests.data_enc1


class BigPrivacyStressTest3(unittest.TestCase):


    def setUp(self):
        
        debug = False
        
        self.graph = BigGraph()
        self.graph.debug = debug
        self.graph.max_links_input = 100000
        self.graph.input_debug_links = 200000
        self.graph.output_debug_nodes = 10000
        use_big_alphabet = False
        self.graph.load_compressed_graph(cloudlight.tests.data_enc1, use_big_alphabet)

        self.graph.create_indices()
        self.graph.create_index_degree()
        self.graph.create_index_unseen_degree()
        self.graph.create_index_triangles()

        lookahead = 1
        coverage = 'korolova node'

        self.strategies = PrivacyAttackStrategies(self.graph, lookahead, coverage, debug)
        
        self.coverages = [0.1] # [ float(f)/100 for f in range(2, 104, 2) ]


    def testStrategyRandom(self):

        #random.seed(6661)
                
        #self.assertEqual( list(self.strategies.start_random([0.01]))[0], 266)
        pass
    

    def testStrategyDegree(self):
        
        random.seed(6662)
                
        self.assertEqual( list(self.strategies.start_degree(self.coverages))[0], 4)
        

    def testStrategyGreedy(self):
        
        random.seed(6663)
                
        self.assertEqual( list(self.strategies.start_greedy(self.coverages))[0], 4)
        

    def testStrategyCrawler(self):
        
        random.seed(6664)
                
        self.assertEqual( list(self.strategies.start_crawler(self.coverages))[0], 4)
        


    def testStrategySupernodeRandom(self):
                
        #random.seed(6665)
                
        #self.assertEqual( list(self.strategies.start_supernode_random([0.01]))[0], 283)
        pass
    

    def testStrategySupernodeDegree(self):
        
        self.assertEqual( list(self.strategies.start_supernode_degree(self.coverages))[0], 6)
        

    def testStrategySupernodeGreedy(self):
        
        self.assertEqual( list(self.strategies.start_supernode_greedy(self.coverages))[0], 6)
        

    def testStrategySupernodeCrawler(self):
        
        self.assertEqual( list(self.strategies.start_supernode_crawler(self.coverages))[0], 16)




if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()