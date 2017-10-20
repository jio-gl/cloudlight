'''
Created on Mar 25, 2010

@author: jose
'''
import unittest

from cloudlight.nodes.search import GoogleQueryNode

class TestSearch(unittest.TestCase):


    def setUp(self):
        self.q = GoogleQueryNode()        
        self.q.context = 'site:facebook.com'
        self.q.search_string = '"Andres Rieznik"'

    def tearDown(self):
        pass


    def testResultsQuery(self):
        
        self.q.update_results_query()
        self.assertTrue( self.q.results > 50 )


    def testLinksQuery(self):
        links = self.q.links_query()
        links.sort()
        self.assertTrue( 'http://www.facebook.com/arieznik' in links )


    def testDistance(self):
        self.q2 = GoogleQueryNode()        
        self.q2.context = 'site:facebook.com'
        self.q2.search_string = '"Martin Rieznik"'

        d = self.q.node_distance(self.q, self.q2)        
        self.assertTrue( d < 0.2 )



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()