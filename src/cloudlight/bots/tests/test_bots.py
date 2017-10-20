'''
Created on Sep 11, 2010

@author: jose
'''
from cloudlight.bots.bot import Bot, CopyBot, PrettyPrintBot
from cloudlight.bots.builder import SumBuilder, NullBuilder
from cloudlight.bots.iterator import NodeIterator, GraphIterator
from cloudlight.bots.visitor import DegreeVisitor
from cloudlight.classes.graph import Graph
from cloudlight.nodes.facebook import FacebookNode, FacebookFriendVisitor
from cloudlight.nodes.node import Node
from cloudlight.nodes.twitter import TwitterNode, TwitterFriendVisitor
import unittest



class Test(unittest.TestCase):


    def setUp(self):
        g = Graph()
        n1 = Node()
        n2 = Node()
        n3 = Node()
        n4 = Node()
        g.add_edge(n1, n2)
        g.add_edge(n2,n3)
        g.add_edge(n3,n1)
        g.add_edge(n3,n4)
        
        self.g = g


    def tearDown(self):
        pass


    def testDegreeSum(self):

        ### Warning! Put class Bot at the end, otherwise it will not work correctly due to subclass resolution order!
        class DegreeBot(NodeIterator, DegreeVisitor, SumBuilder, Bot): pass
    
        bot2 = DegreeBot()
        result2 = bot2.process(self.g)
        self.assertEqual(result2, 8.0)
        
    
    def testCopyBot(self):
        
        bot1 = CopyBot()
        result = bot1.process(self.g)
        
        self.assertEqual(result.number_of_nodes(), 4)
        self.assertEqual(result.number_of_edges(), 4)
        

    def testAdHocVisitor(self):
        
        g = self.g
        
        g.add_node( FacebookNode('Tito Perez') ) 
        g.add_node( TwitterNode('starvejobs') )
    
        class MyVisitor(FacebookVisitor, TwitterVisitor): pass
    
        class MyBot(GraphIterator, MyVisitor, NullBuilder, Bot): pass
        
        bot3 = MyBot()
        result3 = bot3.process(g)
        
        self.assertEqual(result3, None)


    def testPrettyPrint(self):
        
        g = self.g
        
        bot4 = PrettyPrintBot()
        result4 = bot4.process(g)
        
        self.assertEqual(result4, None)
        
        
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()