'''
Created on Jul 20, 2010

@author: jose
'''
import cPickle

'''
Created on Jul 19, 2010

@author: jose
'''
import unittest, pprint

from cStringIO import StringIO

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


    def testPickleDump(self):

        output = StringIO()
        
        self.graph.index_all_parameters()

        self.graph.pickle_dump(output)
        
        obj_rep = output.getvalue()
        
        #self.assertEqual( len(obj_rep),  1650653 )
        graph = cPickle.loads( obj_rep )
        
        self.assertEqual(graph.number_of_nodes(),  43948 )
        self.assertEqual(graph.number_of_edges(),  50000 )        
        
        output.close()
        
        




if __name__ == "__main__":
    unittest.main()