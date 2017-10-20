'''
Created on Jul 19, 2010

@author: jose
'''
import unittest

from cloudlight.classes.graph import Graph
import cloudlight.tests.data_enc1


class Test(unittest.TestCase):


    def setUp(self):
        self.graph = Graph()
        self.graph.debug = False
        self.graph.max_links_input = 50000
        self.graph.input_debug_links = 1000 #200000
        self.graph.output_debug_nodes = 10000
        use_big_alphabet = False
        self.graph.load_compressed_graph(cloudlight.tests.data_enc1, use_big_alphabet, has_num=True)
        
        self.graph.create_indices()


    def tearDown(self):
        pass


    def testDegreeParam(self):

        self.graph.create_index_degree()

        sum = 0 
        for _, value in self.graph.get_parameter_cache_iter('degree'):
            sum += value                     
        self.assertEqual( sum, 100000.0 )
        

    def testClusteringParam(self):

        self.graph.create_index_clustering()
        sum = 0 
        for _, value in self.graph.get_parameter_cache_iter('clustering'):
            sum += value
        self.assertAlmostEqual( sum, 1290.6523256023384 )
        

    def testKnnParam(self):

        self.graph.create_index_knn()
        sum = 0 
        for _, value in self.graph.get_parameter_cache_iter('knn'):
            sum += value                    
        self.assertAlmostEqual( sum, 14815770.85218275 )
        

    def testDegreeInverse(self):

        self.graph.create_index_degree()
        deg_one_nodes = list(self.graph.get_parameter_cache_inverse('degree', 1))
        self.assertEqual( len(deg_one_nodes), 38702 )
        

    def testKnnInverse(self):

        self.graph.create_index_knn()
        deg_one_nodes = list(self.graph.get_parameter_cache_inverse('knn', 139))
        self.assertEqual( len(deg_one_nodes), 381 )
        

    def testClusteringInverse(self):

        self.graph.create_index_clustering()
        deg_one_nodes = list(self.graph.get_parameter_cache_inverse('clustering', 2.0/3))
        
        self.assertEqual( len(deg_one_nodes), 97 )
        
        
    def testGetClustering(self):

        self.graph.create_index_clustering()
        deg_one_nodes = list(self.graph.get_parameter_cache_inverse('clustering', 2.0/3))
        
        node = list(deg_one_nodes)[0]
        self.assertAlmostEqual( self.graph.get_parameter_cache('clustering', node), 2.0/3 )
        
        
        




if __name__ == "__main__":
    unittest.main()