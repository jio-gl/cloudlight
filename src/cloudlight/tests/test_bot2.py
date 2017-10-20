'''
Created on Mar 29, 2010

@author: jose
'''
import unittest

from cloudlight.bots.basic import Constructor, Transform
from cloudlight.nodes.twitter import TwitterNode
from cloudlight.nodes.facebook import FacebookNode
from cloudlight.classes.graph import Graph

class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testComplexTwitterBot(self):

        mynodemap = {
                    str(TwitterNode('AAA').__class__) : TwitterNode.visit_friends
                    }
    
        bot = Transform( mynodemap, None, Constructor() )
        
        graph = Graph()
        graph.add_node( TwitterNode('therm000') )
                
        list(bot.visit( graph ))
            
        self.assertTrue( 'therm000' in map(str, bot.decoratedBot.new_graph.nodes()) )
        self.assertTrue( '89945612' in map(str, bot.decoratedBot.new_graph.nodes()) )        


    def testComplexFacebookBot(self):

        FacebookNode.initialize({}, 'alice.private.life@gmail.com', 'asdfasdf0', False)
        #FacebookNode.initialize({}, 'bob.private.life@gmail.com', 'asdfasdf0', False)

        mynodemap = {
                    str(FacebookNode(1151613578).__class__) : FacebookNode.visit_friends
                    }
    
        bot = Transform( mynodemap, None, Constructor() )
        
        graph = Graph()
        graph.add_node( FacebookNode(1151613578) )
                
        list(bot.visit( graph ))
            
        self.assertTrue( '1151613578' in map(str, bot.decoratedBot.new_graph.nodes()) )
        self.assertTrue( '507271730' in map(str, bot.decoratedBot.new_graph.nodes()) )        



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()