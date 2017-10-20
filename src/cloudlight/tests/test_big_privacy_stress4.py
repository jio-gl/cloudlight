'''
Created on May 11, 2010

@author: jose
'''

import unittest, random

from cloudlight.classes.big_graph import BigGraph
from cloudlight.algorithms.privacy_attack import PrivacyAttackStrategies
import cloudlight.tests.data_enc1


class BigPrivacyStressTest4(unittest.TestCase):


    def setUp(self):
        pass
        self.graph = BigGraph()
        self.graph.debug = False
        self.graph.max_links_input = 5000
        self.graph.input_debug_links = 200000
        self.graph.output_debug_nodes = 500
        use_big_alphabet = False
        self.graph.load_compressed_graph(cloudlight.tests.data_enc1, use_big_alphabet)

        self.graph.create_indices()
        self.graph.remove_degree_cache()
        self.graph.create_index_degree()
        self.graph.index_parameter_from_degree('unseen_degree')
        

        lookahead = 1
        coverage = 'korolova node'

        self.strategies = PrivacyAttackStrategies(self.graph, lookahead, coverage, self.graph.debug)
        
        
        self.coverages = [0.80] # [ float(f)/100 for f in range(2, 104, 2) ]


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
        

    def testStrategySupernodeRandom(self):
        
        random.seed(666)
                
        #self.assertEqual( list(self.strategies.start_supernode_random([0.01]))[0], 51)
        

    def testStrategySupernodeDegree(self):
        
        random.seed(6667)
        
        self.assertEqual( list(self.strategies.start_supernode_degree(self.coverages))[0], 4)
        

    def testStrategySupernodeGreedy(self):
        
        random.seed(6668)
        
        self.assertEqual( list(self.strategies.start_supernode_greedy(self.coverages))[0], 4)
        

    def testStrategySupernodeCrawler(self):
        
        random.seed(6669)
        
        self.assertEqual( list(self.strategies.start_supernode_crawler(self.coverages))[0], 5)


    def testStrategyTriangles(self):
        
        self.graph.create_index_triangles()
        random.seed(7777)

        self.coverages = [0.20]
        self.assertEqual( list(self.strategies.start_triangles(self.coverages))[0], 531)

        
    def testStrategyTrianglesCoverage(self):

        self.graph = BigGraph()
        self.graph.debug = False
        self.graph.max_links_input = 40000 #5000
        self.graph.input_debug_links = 200000
        self.graph.output_debug_nodes = 500
        use_big_alphabet = False
        self.graph.load_compressed_graph(cloudlight.tests.data_enc1, use_big_alphabet)

        self.graph.create_indices()
        self.graph.remove_degree_cache()
        self.graph.create_index_degree()
        self.graph.index_parameter_from_degree('unseen_degree')
        

        lookahead = 1
        coverage = 'korolova node'

        self.strategies = PrivacyAttackStrategies(self.graph, lookahead, coverage, self.graph.debug)
        
        
        self.coverages = [0.80] # [ float(f)/100 for f in range(2, 104, 2) ]

        
        self.graph.create_index_triangles()
        self.graph.index_parameter_from_parameter('triangles', 'unseen_triangles')
        random.seed(7777)

        self.graph.add_edge(1234000, 1234001)
        self.graph.add_edge(1234001, 1234002)
        self.graph.add_edge(1234002, 1234000)

        self.graph.add_edge(1234000, 1234001)
        self.graph.add_edge(1234001, 1234003)
        self.graph.add_edge(1234003, 1234000)

        coverage = 'triangle'
        lookahead = 1

        self.strategies = PrivacyAttackStrategies(self.graph, lookahead, coverage, self.graph.debug)

        self.coverages = [0.80]
        self.assertEqual( list(self.strategies.start_triangles(self.coverages))[0], 28)
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()