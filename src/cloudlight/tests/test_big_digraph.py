'''
Created on Apr 28, 2010

@author: jose
'''
import unittest
from cStringIO import StringIO

from cloudlight.classes.graph import Graph
from cloudlight.classes.big_digraph import BigDiGraph
from cloudlight.tests.data import example_txt


class TestDiGraph(unittest.TestCase):


    def setUp(self):
        self.digraph = BigDiGraph()
        self.digraph.debug = False
        self.digraph.input_debug_links = 1
        self.digraph.output_debug_nodes = 1
        self.digraph.load_edgelist(StringIO(example_txt), num=False)

        self.graph = Graph()
        

    def tearDown(self):
        pass


    def testNodes(self):
        nodes = list(self.digraph.nodes_iter())
        self.assertEqual( nodes, ['1', '2', '3',  '4', '5',  '6', '666', '7', '8', '9'])


    def testNumberOfNodes(self):
        self.assertEqual( self.digraph.number_of_nodes(), 10)


    def testEdges(self):
        edges = list(self.digraph.edges_iter())
        self.assertEqual( len(edges), 11)


    def testEdgesBunch(self):
        edges = list(self.digraph.edges_iter(['1','4']))
        self.assertEqual( len(edges), 2)

    
    def testNumberOfEdges(self):
        self.assertEqual( self.digraph.number_of_edges(), 11)


    def testSymmetricSubgraph(self):
        
        self.digraph.add_only_symmetric_edgelist(self.graph)

        edges = list(self.graph.edges_iter() )
        self.assertEqual( len(edges), 3)
        
        
        
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()