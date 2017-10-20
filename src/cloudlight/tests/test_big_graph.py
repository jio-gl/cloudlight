'''
Created on Apr 20, 2010

@author: jose
'''
import unittest, random
from cStringIO import StringIO

from cloudlight.classes.big_graph import BigGraph
from cloudlight.tests.data import example_txt

class Test(unittest.TestCase):


    def setUp(self):
        
        self.graph = BigGraph()
        self.graph.debug = False
        self.graph.input_debug_links = 1
        self.graph.output_debug_nodes = 1
        self.graph.create_indices()
        self.graph.create_index_clustering()
        self.graph.create_index_degree()
        self.graph.create_index_knn()
        self.graph.load_edgelist(StringIO(example_txt), num=False)
        
        

    def tearDown(self):
        pass

    def testNodes(self):
        nodes = list(self.graph.nodes_iter())
        self.assertEqual( nodes, [u'1', u'2', u'3', u'4', u'5', u'6', u'666', u'7', u'8', u'9'])


    def testEdges(self):
        edges = list(self.graph.edges_iter())
        self.assertEqual( len(edges), 8)

        edges = list(self.graph.edges_iter('9'))
        self.assertEqual( len(edges), 3)

    
    def testEdgesBunch(self):
        edges = list(self.graph.edges_iter(['1','4']))
        self.assertEqual( len(edges), 2)

    
    def testDegrees(self):
        self.assertEqual(list(self.graph.degrees_iter()), [1, 1, 1, 1, 2, 1, 1, 3, 2, 3])


    def testDegreesPartial(self):
        self.assertEqual(list(self.graph.degrees_iter(['2','3','4'])), [1, 1, 1])


    def testClustering(self):

        pass
        #self.assertEqual( list(self.graph.clustering_indices_iter()), [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.33333333333333331, 1.0, 0.33333333333333331])


    def testKnn(self):
        self.assertEqual(list(self.graph.average_neighbor_degrees()), [1.0, 1.0, 2.0, 2.0, 1.0, 3.0, 3.0, 2.0, 3.0, 2.0])


    def testKcorenessIterPartial(self):
        self.assertEqual(list(self.graph.kcoreness_iter(['3', '4', '5'])), [1, 1, 1])

    
    def testEdgeWeight(self):
        
        self.assertEqual( self.graph.degree( '1' ), 1 )
        self.graph.update_edge_weight('1', '2', 0)
        self.assertEqual( self.graph.degree( '1' ), 0 )
        self.assertEqual( self.graph.degree( '1', 0 ), 1 )
        

    def testCountSphere(self):        
        pass
#        self.assertEqual( self.graph.count_edges_lookahead('1', 0), self.graph.degree('1'))
#        self.assertEqual( self.graph.count_edges_lookahead('1', 1), 1)
#        self.graph.add_edge('2', '34')
#        self.graph.add_edge('2', '35')
#        self.assertEqual( self.graph.count_edges_lookahead('1', 1), 3)        
#        self.assertEqual( self.graph.count_edges_lookahead('1', 2), 3)
#        self.graph.add_edge('34', '35')
#        self.assertEqual( self.graph.count_edges_lookahead('1', 2), 4)
#        self.graph.add_edge('34', '3435')
#        self.graph.add_edge('34', '3436')
#        self.graph.add_edge('3435', '3436')
#        self.assertEqual( self.graph.count_edges_lookahead('1', 2), 6)        
#        self.assertEqual( self.graph.count_edges_lookahead('1', 3), 7)


    def testCountSphere2(self):
        self.assertEqual( self.graph.count_nodes_lookahead('1', 0), 2)        
        self.assertEqual( self.graph.count_nodes_lookahead('1', 1), 2)
        self.graph.add_edge('2', '34')
        self.graph.add_edge('2', '35')
        self.assertEqual( self.graph.count_nodes_lookahead('1', 1), 4)        
        self.assertEqual( self.graph.count_nodes_lookahead('1', 2), 4)
        self.graph.add_edge('34', '35')
        self.assertEqual( self.graph.count_nodes_lookahead('1', 2), 4)
        self.graph.add_edge('34', '3435')
        self.graph.add_edge('34', '3436')
        self.assertEqual( self.graph.count_nodes_lookahead('1', 2), 6)        
        self.assertEqual( self.graph.count_nodes_lookahead('1', 3), 6)


    def testCountSphere3(self):
        
        g = BigGraph()

        g.add_node('a')        
        g.add_node('b')
        g.add_node('c')
        g.add_node('d')        
        
        g.add_edge( 'a', 'c' )
        g.add_edge( 'c', 'b' )
        g.add_edge( 'c', 'd' )
        
        self.assertEqual( g.count_edges_lookahead('c', 0), g.degree('c'))
        self.assertEqual( g.count_edges_lookahead('c', 1), g.degree('c'))


    def testSphereIndices(self):
        
        self.graph.create_index_nodesphere(0)
        self.graph.create_index_nodesphere(1)
        self.graph.create_index_nodesphere(2)
        self.graph.create_index_nodesphere(3)

        self.graph.create_index_linksphere(0)
        self.graph.create_index_linksphere(1)
        self.graph.create_index_linksphere(2)
        self.graph.create_index_linksphere(3)
        

    def testCountSphere4(self):
        
        g = BigGraph()

        g.add_node('e')
        g.add_node('a')        
        g.add_node('b')
        g.add_node('c')
        g.add_node('f')
        g.add_node('d')
        g.add_node('g')
        
        
        g.add_edge( 'a', 'c' )
        g.add_edge( 'c', 'b' )
        g.add_edge( 'c', 'd' )
        g.add_edge( 'a', 'f' )
        g.add_edge( 'd', 'e' )
        g.add_edge( 'b', 'g' )
        
        self.assertEqual( g.count_edges_lookahead('c', 0), g.degree('c'))
        
        self.assertEqual( g.count_edges_lookahead('c', 1), 6)


    def testTotalTriangles(self):
        
        self.graph = BigGraph()
        self.graph.create_indices()        
        
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
                
        self.assertEqual(self.graph.total_triangles(), 2)
        
        self.assertEqual(self.graph.total_triangles_weight(1), 2)
        self.assertEqual(self.graph.total_triangles_weight(2), 0)
        
        self.assertEqual(self.graph.triangles_weight(1234000, 1), 2)
        self.assertEqual(self.graph.triangles_weight(1234000, 2), 0)
        self.assertEqual(self.graph.triangles_weight(6756443, 1), 0)
        self.assertEqual(self.graph.triangles_weight(6756443, 2), 0)



if __name__ == "__main__":
    import sys;sys.argv = ['', 'Test.testName']
    unittest.main()