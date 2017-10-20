'''
Created on May 10, 2010

@author: jose
'''

import unittest, random
from StringIO import StringIO

from cloudlight.classes.big_graph import BigGraph
from cloudlight.tests.data import example_txt2
from cloudlight.algorithms.privacy import LinkPrivacyModel
from cloudlight.algorithms.privacy_attack import PrivacyAttackStrategies


class Test(unittest.TestCase):


    def setUp(self):
        self.graph = BigGraph()
        self.graph.debug = False
        self.graph.input_debug_links = 1
        self.graph.output_debug_nodes = 1
        self.graph.load_edgelist(StringIO(example_txt2))
        
        self.graph.create_indices()
        self.graph.create_index_degree()
        self.graph.create_index_unseen_degree()
        self.graph.create_index_triangles()
        
        self.privacy_model = LinkPrivacyModel(self.graph, 1)
        
        
    def setUp2(self):
        
        self.privacy_model.add_bribed_node('RCARecords')
        
        self.assertTrue('RCARecords' in list(self.privacy_model.graph.nodes_iter()) )
                
        self.assertTrue('RCARecords' in self.privacy_model.controlled_nodes )
        
        self.assertAlmostEqual(self.privacy_model.bribe_effort, 1)
        self.assertAlmostEqual(self.privacy_model.total_effort(), 1)


    def tearDown(self):
        pass


    def testAddBribedNode(self):
        
        self.setUp2()

        self.assertEqual(self.privacy_model.korolova_node_coverage(), 0.045454545454545456)

        self.privacy_model.add_bribed_node('jcl5m')
        
        self.assertEqual(self.privacy_model.korolova_node_coverage(), 0.47727272727272729)
        

    def testAddRogueNode(self):
        
        self.privacy_model.add_rogue_node('Rogue1')
                
        self.assertEqual(self.privacy_model.controlled_nodes, set(['Rogue1']) )
        self.assertTrue('Rogue1' in list(self.privacy_model.graph.nodes_iter()) )
        self.assertEqual( list(self.privacy_model.graph.edges_iter('Rogue1')), [] )
        
        self.assertEqual(list(self.privacy_model.graph.edges_iter('Rogue1')), [] )

        self.assertAlmostEqual(self.privacy_model.rogue_effort, 1)


    def testMaxUnseenDegreeNode(self):
        
        self.setUp2()

        self.assertEqual( self.privacy_model.max_unseen_degree_node(), 'ABadFeeling')
        
        
    def testMaxUnseenDegreeCrawlerNode(self):
        
        self.setUp2()

        self.privacy_model.add_bribed_node('Egger3rd')

        self.assertEqual( self.privacy_model.max_unseen_degree_crawler_node(), 'cjweeks')
        


    def testSortedDegreesDec(self):
        
        
        self.assertEqual( list(self.privacy_model.sorted_degrees_dec_iter())[:2], ['ABadFeeling', 'Egger3rd'])


    def testActiveAttack(self):
        
        self.graph = BigGraph()
        g = self.graph
        
        g.add_edge( '3', '1')
        g.add_edge( '4', '1')
        g.add_edge( '5', '1')
        g.add_edge( '6', '5')
        g.add_edge( '2', '7')
        g.add_edge( '8', '2')
        g.add_edge( '9', '2')
        
        self.assertEqual( list(self.graph.neighbors_iter( '1' )), [u'3', u'4', u'5'] )
        
        self.graph.create_indices()
        self.graph.create_index_degree()
        self.graph.create_index_unseen_degree()

        self.privacy_model = LinkPrivacyModel(self.graph, 2)

        self.privacy_model.add_bribed_node( '5' )
        
        self.assertEqual(self.privacy_model.korolova_node_coverage(), 0.55555555555555558)
        
        self.privacy_model.add_false_link( '1', '2')

        self.assertEqual( set(self.graph.neighbors_iter( '1' )), set([u'3', u'4', u'5', u'2', ]) )
        
        self.assertEqual(self.privacy_model.korolova_node_coverage(), 1.0)
        

    def testHistogram(self):
        
        self.privacy_model.initialize_histogram_degree(degree_dist=lambda x : 0.677 * x**-2.33, number_of_nodes=100000)
        
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()