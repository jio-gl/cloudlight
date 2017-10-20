'''
Created on Apr 26, 2010

@author: jose
'''
import unittest, random

from cloudlight.classes.graph import Graph
import cloudlight.tests.data_enc1


class GraphTest3(unittest.TestCase):


    def setUp(self):
        self.graph = Graph()
        self.graph.debug = False
        self.graph.max_links_input = 50000
        self.graph.input_debug_links = 200000
        self.graph.output_debug_nodes = 10000
        use_big_alphabet = False
        has_num = False
        self.graph.load_compressed_graph(cloudlight.tests.data_enc1, use_big_alphabet, has_num)

        
    def tearDown(self):
        pass


    def testNodes(self):
        self.assertEqual( self.graph.number_of_nodes(), 43948 )


    def testEdges(self):
        self.assertEqual( self.graph.number_of_edges(), 50000 )


    def testDegreesPartial(self):
        self.assertEqual(list(self.graph.degrees_iter(['2','3','4'])), [606, 595, 551])


    def testClustering(self):
        self.assertEqual(list(self.graph.clustering_indices_iter(['2','274','1174','278'])), [0.0, 0.025062656641604009, 0.33333333333333331, 0.024025974025974027])


    def testKnn(self):
        self.assertEqual(list(self.graph.average_neighbor_degrees_iter(['2','274','1174','278'])), [1.2854785478547854, 4.5087719298245617, 329.33333333333331, 6.3214285714285712])


    def testKcorenessIterPartial1(self):
        self.assertEqual(list(self.graph.kcoreness_iter(['2','274','1174','278'])), [4, 3, 3, 3])

    def testKcorenessIterPartial2(self):
        self.assertEqual(list(self.graph.kcoreness_iter(['3', '4', '5'])), [5, 4, 4])


    def testTriangles(self):        

        self.graph.add_edge('2','1234000')
        self.graph.add_edge('1234000', '1234001')
        self.graph.add_edge('1234001', '2')
        
        self.graph.add_edge('2','1')
        self.graph.add_edge('1', '1234001')
        self.graph.add_edge('1234001', '2')
        
        self.graph.add_edge('2','1234003')
        self.graph.add_edge('1234003', '1234004')
        self.graph.add_edge('1234004', '2')

        self.assertEqual(list(self.graph.triangles_iter(['2','3', '4'])), [3, 0, 25])


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
