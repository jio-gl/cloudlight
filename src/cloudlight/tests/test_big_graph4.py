'''
Created on May 18, 2010

@author: jose
'''
import unittest, random
from cStringIO import StringIO

from cloudlight.classes.big_graph import BigGraph

class Test(unittest.TestCase):


    def setUp(self):
        
        self.graph = BigGraph()
        self.graph.debug = False
        self.graph.input_debug_links = 1
        self.graph.output_debug_nodes = 1

        for i in range(5):
            self.graph.add_edge(str(i), str(i+1))
            self.graph.add_edge(str(-i), str(-i-1))
        
        self.graph.create_indices()
        
        

    def tearDown(self):
        pass


#    def testNeighborhoodLookahead0(self):
#        
#        lookahead = 0
#        self.assertEqual( list(self.graph.edges_neighborhood('0', lookahead)), [(u'0', u'1'), (u'0', u'-1')])
#        
#
#    def testNeighborhoodLookahead1(self):
#        
#        lookahead = 1
#        self.assertEqual( list(self.graph.edges_neighborhood('0', lookahead)), [(u'0', u'1'), (u'0', u'-1'), (u'1', u'2'), (u'-1', u'-2')])
#        
#
#    def testNeighborhoodLookahead2(self):
#        
#        lookahead = 2
#        self.assertEqual( list(self.graph.edges_neighborhood('0', lookahead)), [(u'0', u'1'), (u'0', u'-1'), (u'1', u'2'), (u'-1', u'-2'), (u'2', u'3'), (u'-2', u'-3')])
#        
#
#    def testNeighborhoodLookahead3(self):
#        
#        lookahead = 3
#        self.assertEqual( list(self.graph.edges_neighborhood('0', lookahead)), [(u'0', u'1'), (u'0', u'-1'), (u'1', u'2'), (u'-1', u'-2'), (u'2', u'3'), (u'-2', u'-3'), (u'3', u'4'), (u'-3', u'-4')] )
#        
#
#    def testNeighborhoodUpdate(self):
#        
#        self.graph.create_index_degree()
#        
#        param = 'unseen_degree'
#        self.__unseen_param_key = param
#        
#        self.graph.remove_index_parameter_cache(self.__unseen_param_key)
#        self.graph.remove_parameter_cache(self.__unseen_param_key)
#        
#        self.graph.add_parameter_cache(self.__unseen_param_key)
#        
#        for node, degree in self.graph.get_parameter_cache_iter('degree'):
#            
#            self.graph.insert_parameter_cache(self.__unseen_param_key, node, degree)
#       
#        self.graph.index_parameter_cache( self.__unseen_param_key )
#        
#        lookahead = 0
#        
#        self.graph.reset_edge_weights()
#        
#        self.assertEqual( self.graph.get_parameter_cache(param, '0'), 2.0 )
#        self.assertEqual( self.graph.get_parameter_cache(param, '1'), 2.0 )
#        
#        self.graph.dec_neighborhood_parameter('0', lookahead, param)
#        self.graph.update_neighborhood_lookahead('0', lookahead)
#        
#        self.assertEqual( self.graph.get_parameter_cache(param, '0'), 0.0 )
#        self.assertEqual( self.graph.get_parameter_cache(param, '1'), 1.0 )
#        
#
#    def testNeighborhoodUpdate1(self):
#        
#        self.graph.create_index_degree()
#        
#        param = 'unseen_degree'
#        self.__unseen_param_key = param
#        
#        self.graph.remove_index_parameter_cache(self.__unseen_param_key)
#        self.graph.remove_parameter_cache(self.__unseen_param_key)
#        
#        self.graph.add_parameter_cache(self.__unseen_param_key)
#        
#        for node, degree in self.graph.get_parameter_cache_iter('degree'):
#            
#            self.graph.insert_parameter_cache(self.__unseen_param_key, node, degree)
#       
#        self.graph.index_parameter_cache( self.__unseen_param_key )
#        
#        lookahead = 1
#        
#        self.graph.reset_edge_weights()
#        
#        self.assertEqual( self.graph.get_parameter_cache(param, '0'), 2.0 )
#        self.assertEqual( self.graph.get_parameter_cache(param, '1'), 2.0 )
#        
#        self.graph.dec_neighborhood_parameter('0', lookahead, param)
#        self.graph.update_neighborhood_lookahead('0', lookahead)
#        
#        self.assertEqual( self.graph.get_parameter_cache(param, '0'), 0.0 )
#        self.assertEqual( self.graph.get_parameter_cache(param, '1'), 0.0 )
#        self.assertEqual( self.graph.get_parameter_cache(param, '2'), 1.0 )
#        
#
#    def testNeighborhoodUpdate2(self):
#        
#        self.graph.create_index_degree()
#        
#        param = 'unseen_degree'
#        self.__unseen_param_key = param
#        
#        self.graph.remove_index_parameter_cache(self.__unseen_param_key)
#        self.graph.remove_parameter_cache(self.__unseen_param_key)
#        
#        self.graph.add_parameter_cache(self.__unseen_param_key)
#        
#        for node, degree in self.graph.get_parameter_cache_iter('degree'):
#            
#            self.graph.insert_parameter_cache(self.__unseen_param_key, node, degree)
#       
#        self.graph.index_parameter_cache( self.__unseen_param_key )
#        
#        lookahead = 2
#        
#        self.graph.reset_edge_weights()
#        
#        self.assertEqual( self.graph.get_parameter_cache(param, '0'), 2.0 )
#        self.assertEqual( self.graph.get_parameter_cache(param, '1'), 2.0 )
#        self.assertEqual( self.graph.get_parameter_cache(param, '2'), 2.0 )
#        self.assertEqual( self.graph.get_parameter_cache(param, '3'), 2.0 )
#        
#        
#        self.graph.dec_neighborhood_parameter('0', lookahead, param)
#        self.graph.update_neighborhood_lookahead('0', lookahead)
#        
#        self.assertEqual( self.graph.get_parameter_cache(param, '0'), 0.0 )
#        self.assertEqual( self.graph.get_parameter_cache(param, '1'), 0.0 )
#        self.assertEqual( self.graph.get_parameter_cache(param, '2'), 0.0 )
#        self.assertEqual( self.graph.get_parameter_cache(param, '3'), 1.0 )
#        
#
#    def testNeighborhoodUpdate3(self):
#        
#        self.graph.create_index_degree()
#        
#        param = 'unseen_degree'
#        self.__unseen_param_key = param
#        
#        self.graph.remove_index_parameter_cache(self.__unseen_param_key)
#        self.graph.remove_parameter_cache(self.__unseen_param_key)
#        
#        self.graph.add_parameter_cache(self.__unseen_param_key)
#        
#        for node, degree in self.graph.get_parameter_cache_iter('degree'):
#            
#            self.graph.insert_parameter_cache(self.__unseen_param_key, node, degree)
#       
#        self.graph.index_parameter_cache( self.__unseen_param_key )
#        
#        lookahead = 3
#        
#        self.graph.reset_edge_weights()
#        
#        self.assertEqual( self.graph.get_parameter_cache(param, '0'), 2.0 )
#        self.assertEqual( self.graph.get_parameter_cache(param, '1'), 2.0 )
#        self.assertEqual( self.graph.get_parameter_cache(param, '2'), 2.0 )
#        self.assertEqual( self.graph.get_parameter_cache(param, '3'), 2.0 )
#        
#        
#        self.graph.dec_neighborhood_parameter('0', lookahead, param)
#        self.graph.update_neighborhood_lookahead('0', lookahead)
#        
#        self.assertEqual( self.graph.get_parameter_cache(param, '0'), 0.0 )
#        self.assertEqual( self.graph.get_parameter_cache(param, '1'), 0.0 )
#        self.assertEqual( self.graph.get_parameter_cache(param, '2'), 0.0 )
#        self.assertEqual( self.graph.get_parameter_cache(param, '3'), 0.0 )
#        self.assertEqual( self.graph.get_parameter_cache(param, '4'), 1.0 )
        





if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()