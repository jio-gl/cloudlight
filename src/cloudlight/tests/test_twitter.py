'''
Created on Mar 18, 2010

@author: jose
'''
import unittest, base64, urllib2, time

from cloudlight.classes.graph import Graph
from cloudlight.nodes.twitter import TwitterNode, TwitterControlledNode
from cloudlight.tests.jpg import jpg


class TwitterNodeTest(unittest.TestCase):

    user_show_xml = 'http://api.twitter.com/1/users/show.xml?screen_name=%s'

    def setUp(self):
        self.node = TwitterNode(screen_name='_berniemadoff_')
        

    def tearDown(self):
        pass
        #self.g.save_edgelist(open('twitter.txt', 'w'))


    def testVisitFriends(self):
    
        g = Graph()
        g.add_node(self.node)
        
        friends = self.node.friends()
        self.assertEqual(set(map(str, friends)), set(['3108351', '26601797', '18149408', '19253848', '36544954', '75970385', '18114931', '55463984', '19732920', '42917391', '25566068', '25925954', '44674512', '19305701', '45712556']))

        self.g = g
        
        
    def testControlledNode1(self):
        
        screen_name = 'mc40mdcx'
        passwd = 'asdfasdf'            
        node = TwitterControlledNode(screen_name, screen_name, passwd, create=False)
        
        jpg_url = '/tmp/test_twitter.jpg' 
        f = open(jpg_url, 'w')
        f.write( base64.b64decode( jpg ) )
        f.close()
        
        node.set_profile_image_url(jpg_url)
        time.sleep(2.0)
        
        user_html = urllib2.urlopen('http://twitter.com/' + node.screen_name).read()
        self.assertTrue( 'test_twitter_bigger.jpg' in user_html )




if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
