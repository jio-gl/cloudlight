'''
Created on Apr 26, 2010

@author: jose
'''
import unittest

from cloudlight.classes.big_graph import BigGraph
import cloudlight.tests.data_enc1


class BigGraphTest3(unittest.TestCase):


    def setUp(self):
        
        self.graph = BigGraph()
        self.graph.debug = False
        self.graph.max_links_input = 20000
        self.graph.input_debug_links = 200000
        self.graph.output_debug_nodes = 10000
        use_big_alphabet = False
        self.graph.load_compressed_graph(cloudlight.tests.data_enc1, use_big_alphabet, has_num=True)
        
        self.graph.create_indices()
        self.graph.create_index_kcores()
        
        pass

        
    def tearDown(self):
        pass


    def testNodes(self):
        self.assertEqual( self.graph.number_of_nodes(), 18284 )


    def testEdges(self):
        self.assertEqual( self.graph.number_of_edges(), 20000 )


    def testDegreesPartial(self):
        self.assertEqual(list(self.graph.degrees_iter(['2','3','4'])), [606, 595, 551])


    def testClustering(self):      
        self.assertEqual(list(self.graph.clustering_indices_iter(['4071','274','1174','278','2'])), [1.0, 0.0, 0.0, 0.0, 0.0])


    def testKnn(self):
        self.assertEqual(list(self.graph.average_neighbor_degrees_iter(['2','274','1174','278'])), [1.2112211221122111, 0.0, 870.0, 0.0])


    def testKcorenessIterPartial1(self):
        self.assertEqual(list(self.graph.kcoreness_iter(['2','1174'])), [4, 1])

    def testKcorenessIterPartial2(self):
        self.assertEqual(list(self.graph.kcoreness_iter(['3', '4', '5'])), [4, 4, 4])


    def testTriangles(self):        

        #self.graph = BigGraph()
        #self.graph.create_indices()
        
        self.graph.add_edge('2','1234000')
        self.graph.add_edge('1234000', '1234001')
        self.graph.add_edge('1234001', '2')
        
        self.graph.add_edge('2','1')
        self.graph.add_edge('1', '1234001')
        self.graph.add_edge('1234001', '2')
        
        self.graph.add_edge('2','1234003')
        self.graph.add_edge('1234003', '1234004')
        self.graph.add_edge('1234004', '2')

        self.graph.add_edge('2','1234003')
        self.graph.add_edge('1234003', '1234006')
        self.graph.add_edge('1234006', '2')

        self.graph.create_index_triangles()  
        self.assertEqual(list(self.graph.triangles_iter(['2','274','1174','278'])), [4, 0, 0, 0])
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
