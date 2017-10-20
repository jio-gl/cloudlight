'''
Created on Mar 19, 2010

@author: jose
'''

import unittest, random
from StringIO import StringIO

from cloudlight.classes.big_graph import BigGraph
from cloudlight.tests.data import example_txt2
from cloudlight.algorithms.privacy_attack import LinkPrivacyModel


class Test(unittest.TestCase):


    def setUp(self):
        self.graph = BigGraph()
        self.graph.debug = False
        self.graph.input_debug_links = 1
        self.graph.output_debug_nodes = 1
        self.graph.load_edgelist(StringIO(example_txt2))
        
        self.graph.create_indices()
        self.graph.create_index_degree()
        self.graph.create_index_triangles()
        self.graph.create_index_unseen_degree()
        self.graph.index_parameter_from_parameter('triangles', 'unseen_triangles')
        self.graph.add_parameter_cache('seen_degree')
        self.graph.initialize_parameter('seen_degree', 0.0)
        self.graph.index_parameter_cache('seen_degree')
        self.graph.add_parameter_cache('seen_degree2')
        self.graph.initialize_parameter('seen_degree2', 0.0)
        self.graph.index_parameter_cache('seen_degree2')
        self.graph.add_parameter_cache('seen_triangles')
        self.graph.initialize_parameter('seen_triangles', 0.0)
        self.graph.index_parameter_cache('seen_triangles')
        self.graph.add_parameter_cache('seen_triangles2')
        self.graph.initialize_parameter('seen_triangles2', 0.0)
        self.graph.index_parameter_cache('seen_triangles2')
        
        self.privacy_model = LinkPrivacyModel(self.graph, 1)
        self.privacy_model.coverage_types = ['node','korolova','link','triangle']

        
    def setUp2(self):
        self.privacy_model.add_bribed_node('RCARecords')
        
        self.assertTrue('RCARecords' in self.privacy_model.graph.nodes_iter() )
                
        self.assertTrue(not 'RCARecords' in self.privacy_model.agents )
        self.assertTrue('RCARecords' in self.privacy_model.controlled_nodes )
        
        self.assertAlmostEqual(self.privacy_model.bribe_effort, 1)
        self.assertAlmostEqual(self.privacy_model.total_effort(), 1)

        self.privacy_model.strategy = 'start_crawler'
        self.privacy_model.add_bribed_node('foofighters')




    def tearDown(self):
        pass


#    def testAddRogueNode(self):
#        
#        pass
#
#    def testCoverage(self):
#        
#        self.setUp2()
#
#        self.assertEqual( self.privacy_model.link_coverage(), 0.51162790697674421)
#        
#        
#    def testMaxUnseenDegreeNode(self):
#        
#        self.setUp2()
#
#        self.assertEqual( self.privacy_model.max_unseen_degree_node(), 'Egger3rd')
#        
#        
#    def testMaxUnseenDegreeCrawlerNode(self):
#        
#        self.setUp2()
#
#        self.privacy_model.add_bribed_node('Egger3rd')
#
#        self.assertEqual( self.privacy_model.max_unseen_degree_crawler_node(), 'cjweeks')
#        
#
#    def testSortedDegreesDec(self):
#        
#        self.assertEqual( list(self.privacy_model.sorted_degrees_dec_iter())[:4], ['ABadFeeling', 'Egger3rd', 'cjweeks', 'foofighters'])
#        self.assertEqual( sorted(list(self.privacy_model.sorted_degrees_dec_iter())), sorted(list(set( self.privacy_model.sorted_degrees_dec_iter() ))) ) 




    def setUp3(self):
        self.graph = BigGraph()
        self.graph.debug = False
        self.graph.input_debug_links = 1
        self.graph.output_debug_nodes = 1

        edge = self.graph.add_edge
        a,b,c,d,e,f,g,h,i = 'a','b','c','d','e','f','g','h','i'
        
        edge(a,b)
        edge(b,c)
        edge(c,e)
        edge(c,d)
        edge(d,e)
        edge(b,d)
        edge(a,f)
        edge(a,g)
        edge(a,h)
        edge(a,i)
        edge(g,h)
        edge(h,i)
        
        self.graph.create_indices()
        self.graph.create_index_degree()
        self.graph.create_index_triangles()
        self.graph.create_index_unseen_degree()
        self.graph.index_parameter_from_parameter('triangles', 'unseen_triangles')
        self.graph.add_parameter_cache('seen_degree')
        self.graph.initialize_parameter('seen_degree', 0.0)
        self.graph.index_parameter_cache('seen_degree')
        self.graph.add_parameter_cache('seen_degree2')
        self.graph.initialize_parameter('seen_degree2', 0.0)
        self.graph.index_parameter_cache('seen_degree2')
        self.graph.add_parameter_cache('seen_triangles')
        self.graph.initialize_parameter('seen_triangles', 0.0)
        self.graph.index_parameter_cache('seen_triangles')
        self.graph.add_parameter_cache('seen_triangles2')
        self.graph.initialize_parameter('seen_triangles2', 0.0)
        self.graph.index_parameter_cache('seen_triangles2')
        
        
        self.privacy_model = LinkPrivacyModel(self.graph, 1)
        self.privacy_model.coverage_types = ['node','korolova','link','triangle']
        self.privacy_model.initialize_histogram_degree(number_of_nodes=self.graph.number_of_nodes())
        self.privacy_model.strategy = 'start_crawler_degree_hist'        
        
    def testBribedNodeRecursive(self):
        
        self.setUp3()
        g = self.graph
        
        self.assertEqual( g.get_parameter_cache('seen_degree', 'a') , 0 )
        self.assertEqual( g.get_parameter_cache('seen_degree2', 'a') , 0 )
        self.assertEqual( g.get_parameter_cache('unseen_degree', 'a') , 5 )
        self.assertEqual( g.get_parameter_cache('seen_triangles', 'a') , 0 )
        self.assertEqual( g.get_parameter_cache('seen_triangles2', 'a') , 0 )
        self.assertEqual( g.get_parameter_cache('unseen_triangles', 'a') , 2 )
        
        self.assertEqual( g.get_parameter_cache('seen_degree', 'b') , 0 )
        self.assertEqual( g.get_parameter_cache('seen_degree2', 'b') , 0 )
        self.assertEqual( g.get_parameter_cache('unseen_degree', 'b') , 3 )
        self.assertEqual( g.get_parameter_cache('seen_triangles', 'b') , 0 )
        self.assertEqual( g.get_parameter_cache('seen_triangles2', 'b') , 0 )
        self.assertEqual( g.get_parameter_cache('unseen_triangles', 'b') , 1 )
        
        self.assertEqual( self.privacy_model.M, [9, 0, 0, 0, 0, 0] )

        #print 'SOBORNANDO NODO "a"'
        self.privacy_model.add_bribed_node('a')

        self.assertEqual( g.get_parameter_cache('seen_degree', 'a') , -1 )
        self.assertEqual( g.get_parameter_cache('seen_degree2', 'a') , 5 )
        self.assertEqual( g.get_parameter_cache('unseen_degree', 'a') , 0 )
        self.assertEqual( g.get_parameter_cache('seen_triangles', 'a') , 2 )
        self.assertEqual( g.get_parameter_cache('seen_triangles2', 'a') , -1 )
        self.assertEqual( g.get_parameter_cache('unseen_triangles', 'a') , 0 )
        
        self.assertEqual( g.get_parameter_cache('seen_degree', 'b') , -1 )
        self.assertEqual( g.get_parameter_cache('seen_degree2', 'b') , 3 )
        self.assertEqual( g.get_parameter_cache('unseen_degree', 'b') , 0 )
        self.assertEqual( g.get_parameter_cache('seen_triangles', 'b') , 0 )
        self.assertEqual( g.get_parameter_cache('seen_triangles2', 'b') , 0 )
        self.assertEqual( g.get_parameter_cache('unseen_triangles', 'b') , 1 )

        self.assertEqual( self.privacy_model.M, [1, 3, 2, 2, 0, 1] )

        #print 'SOBORNANDO NODO "a"'
        self.privacy_model.add_bribed_node('b')

        self.assertEqual( g.get_parameter_cache('seen_degree', 'b') , -1 )
        self.assertEqual( g.get_parameter_cache('seen_degree2', 'b') , 3 )
        self.assertEqual( g.get_parameter_cache('unseen_degree', 'b') , 0 )
        self.assertEqual( g.get_parameter_cache('seen_triangles', 'b') , 1 )
        self.assertEqual( g.get_parameter_cache('seen_triangles2', 'b') , -1 )
        self.assertEqual( g.get_parameter_cache('unseen_triangles', 'b') , 0 )

        self.assertEqual( self.privacy_model.M, [0, 1, 3, 4, 0, 1] )

        self.assertEqual( self.privacy_model.link_coverage(), 1.0 )




        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()