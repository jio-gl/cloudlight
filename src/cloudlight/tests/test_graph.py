'''
Created on Mar 16, 2010

@author: jose
'''
import unittest, random
from cStringIO import StringIO

from cloudlight.classes.graph import Graph
from cloudlight.tests.data import example_txt, top_edges


class GraphTest(unittest.TestCase):


    def setUp(self):
        self.graph = Graph()
        self.graph.debug = False
        self.graph.input_debug_links = 1
        self.graph.output_debug_nodes = 1
        self.graph.load_edgelist(StringIO(example_txt), num=False)
        
    def tearDown(self):
        pass


#    def testNodes(self):
#        nodes = list(self.graph.nodes_iter())
#        self.assertEqual( nodes, ['666', '1', '3', '2', '5', '4', '7', '6', '9', '8'])
#
#
#    def testEdges(self):
#        edges = list(self.graph.edges_iter())
#        self.assertEqual( len(edges), 8)
#
#
#    def testEdgesBunch(self):
#        edges = list(self.graph.edges_iter(['1','4']))
#        self.assertEqual( len(edges), 2)
#
#    
#    def testDegrees(self):
#        self.assertEqual(list(self.graph.degrees()), [1, 1, 1, 1, 2, 1, 3, 1, 3, 2])
#
#
#    def testDegreesPartial(self):
#        self.assertEqual(list(self.graph.degrees(['2','3','4'])), [1, 1, 1])
#
#
#    def testDegreesIter(self):
#        self.assertEqual(list(self.graph.degrees_iter()), [1, 1, 1, 1, 2, 1, 3, 1, 3, 2])
#
#
#    def testClustering(self):
#        self.assertEqual(list(self.graph.clustering_indices()), [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.33333333333333331, 0.0, 0.33333333333333331, 1.0])
#
#
#    def testKnn(self):
#        self.assertEqual(list(self.graph.average_neighbor_degrees()), [3.0, 1.0, 2.0, 1.0, 1.0, 2.0, 2.0, 3.0, 2.0, 3.0])
#
#
#    def testExcentricity(self):
#        self.assertEqual(list(self.graph.eccentricities()), [3, 1, 2, 1, 1, 2, 2, 3, 2, 2])
#
#
#    def testAveragePathLengths(self):
#        self.assertEqual(list(self.graph.average_path_lengths()), [1.6000000000000001, 0.5, 1.0, 0.5, 0.66666666666666663, 1.0, 1.0, 1.6000000000000001, 1.0, 1.2])
#
#
#    def testKcoreness(self):
#        self.assertEqual(list(self.graph.kcoreness()), [1, 1, 1, 1, 1, 1, 2, 1, 2, 2])
#
#
#    def testKcorenessPartial(self):
#        self.assertEqual(list(self.graph.kcoreness(['3', '4', '5'])), [1, 1, 1])
#
#
#    def testKcorenessIterPartial(self):
#        self.assertEqual(list(self.graph.kcoreness_iter(['3', '4', '5'])), [1, 1, 1])
#
#
#    def testRandomEdges(self):
#        random.seed(666)
#        self.assertEqual(self.graph.random_edges(2, False), [('666', '9'), ('3', '5')])
#        
#
#    def testRandomNodes(self):
#        random.seed(666)
#        self.assertEqual(self.graph.random_nodes(3, False), ['4', '2', '666'])
#        
#
#    def testShow(self):
##        self.graph = Graph()
##        self.graph.debug = False
##        self.graph.input_debug_links = 1
##        self.graph.output_debug_nodes = 1
##        self.graph.load_edgelist(StringIO(top_edges), num=False)
##        self.graph.show()
#        pass
#    
#    def testDegreeEncodedGraph(self):        
#
#        self.assertEqual(self.graph.compressed_by_degree_graph().nodes(), ['!', '"', '%', '$', "'", '&', ')', '(', '+', '*'])
#        self.assertEqual(self.graph.compressed_by_degree_graph().degrees(), [3, 3, 2, 2, 1, 1, 1, 1, 1, 1])
#
#    
#    def testSaveEncoded1(self):
#        enc_g = self.graph.compressed_by_degree_graph(False)
#        io = StringIO()
#        enc_g.save_edgelist(io)
#        self.assertEqual( io.getvalue().split('\n')[2:], ['# ', '0 9', '0 2', '0 1', '1 2', '1 4', '3 5', '3 7', '6 8', ''])
#
#
#    def testSaveEncoded2(self):
#        enc_g = self.graph.compressed_by_degree_graph()
#        io = StringIO()
#        enc_g.save_edgelist(io)
#        self.assertEqual( io.getvalue().split('\n')[2:], ['# ', '! +', '! "', '! $', '" $', '" &', '% )', "% '", '( *', ''])


#    def testTotalTriangles(self):
#        
#        self.assertEqual(self.graph.total_triangles(), 1)
#        self.assertEqual(self.graph.total_triangles_weight(1), 1)
#        self.assertEqual(self.graph.total_triangles_weight(2), 0)
#        
#        self.graph.add_edge(1234000, 1234001)
#        self.graph.add_edge(1234001, 1234002)
#        self.graph.add_edge(1234002, 1234000)
#
#        self.graph.add_edge(1234000, 1234001)
#        self.graph.add_edge(1234001, 1234003)
#        self.graph.add_edge(1234003, 1234000)
#        
#        self.assertEqual(self.graph.total_triangles(), 3)
#        self.assertEqual(self.graph.total_triangles_weight(1), 3)
#        self.assertEqual(self.graph.total_triangles_weight(2), 0)
#        
#        self.assertEqual(self.graph.triangles_weight(1234000, 1), 2)
#        self.assertEqual(self.graph.triangles_weight(1234000, 2), 0)
#        self.assertEqual(self.graph.triangles_weight(6756443, 1), 0)
#        self.assertEqual(self.graph.triangles_weight(6756443, 2), 0)
#
#        self.graph.update_edge_weight(1234000, 1234001, 2)
#        self.graph.update_edge_weight(1234001, 1234003, 2)
#        self.graph.update_edge_weight(1234003, 1234000, 2)
#
#        self.assertEqual(self.graph.total_triangles(), 3)        
#        self.assertEqual(self.graph.total_triangles_weight(1), 1)
#        self.assertEqual(self.graph.total_triangles_weight(2), 1)
#
#        self.assertEqual(self.graph.triangles_weight(1234000, 1), 0)
#        self.assertEqual(self.graph.triangles_weight(1234000, 2), 1)
#        self.assertEqual(self.graph.triangles_weight(6756443, 1), 0)
#        self.assertEqual(self.graph.triangles_weight(6756443, 2), 0)
#
#        self.graph.update_edge_weight(1234000, 1234001, 2)
#        self.graph.update_edge_weight(1234001, 1234002, 2)
#        self.graph.update_edge_weight(1234002, 1234000, 2)
#
#        self.assertEqual(self.graph.total_triangles(), 3)
#        self.assertEqual(self.graph.total_triangles_weight(1), 1)
#        self.assertEqual(self.graph.total_triangles_weight(2), 2)
#        
#        self.assertEqual(self.graph.triangles_weight(1234000, 1), 0)
#        self.assertEqual(self.graph.triangles_weight(1234000, 2), 2)
#        self.assertEqual(self.graph.triangles_weight(6756443, 1), 0)
#        self.assertEqual(self.graph.triangles_weight(6756443, 2), 0)


    def testTotalTriangles(self):
        
        self.graph = Graph()
        
        self.graph.add_edge(1234000, 1234001)
        self.graph.add_edge(1234001, 1234002)
        self.graph.add_edge(1234002, 1234000)

        self.graph.add_edge(1234000, 1234001)
        self.graph.add_edge(1234001, 1234003)
        self.graph.add_edge(1234003, 1234000)
        
        self.graph.create_index_triangles()
        
        self.assertEqual(self.graph.get_parameter_cache('triangles', 1234000), 2)
        self.assertEqual(self.graph.get_parameter_cache('triangles', 1234001), 2)
        self.assertEqual(self.graph.get_parameter_cache('triangles', 1234002), 1)
        self.assertEqual(self.graph.get_parameter_cache('triangles', 1234003), 1)
        
                
        print
        for node, value in self.graph.get_parameter_cache_iter('triangles'):
            print node, value

        self.assertEqual(self.graph.total_triangles(), 2)
        
        
        self.assertEqual(self.graph.total_triangles_weight(1), 2)
        self.assertEqual(self.graph.total_triangles_weight(2), 0)
        
        self.assertEqual(self.graph.triangles_weight(1234000, 1), 2)
        self.assertEqual(self.graph.triangles_weight(1234000, 2), 0)
        self.assertEqual(self.graph.triangles_weight(6756443, 1), 0)
        self.assertEqual(self.graph.triangles_weight(6756443, 2), 0)

    
    def testTotalTrianglesWeight(self):
        
        g = Graph()

        g.add_edge(1,2)
        g.add_edge(2,3)
        g.add_edge(3,1)
        
        g.add_edge(5,6)
        g.add_edge(6,7)
        g.add_edge(7,5)

        g.create_index_triangles()
        g.index_parameter_from_parameter('triangles', 'unseen_triangles')

        self.assertEqual(g.total_triangles_weight(1), 2)
        self.assertEqual(g.total_triangles_weight(2), 0)
        self.assertEqual(g.total_unseen_triangles(), 2)

        g.update_edge_weight(1, 2, 2)

        self.assertEqual(g.total_triangles_weight(1), 1)
        self.assertEqual(g.total_triangles_weight(2), 0)

        g.update_edge_weight(2, 3, 2)
        g.update_edge_weight(3, 1, 2)

        self.assertEqual(g.total_triangles_weight(1), 1)
        self.assertEqual(g.total_triangles_weight(2), 1)
        



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
