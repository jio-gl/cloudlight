'''
Created on Apr 9, 2010

@author: jose
'''
import unittest


from cloudlight.nodes.web import UrlNode


class WebTest(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testUrl1(self):
        myurl = UrlNode('http://tuplets.org')
        self.assertEqual( myurl.protocol(), 'http')
        self.assertEqual( myurl.domain(), 'tuplets.org')
        self.assertEqual( myurl.resource(), '/')

    
    def testUrl2(self):
        myurl = UrlNode('https://www.search.com/search?q=zarasa%20bla')
        self.assertEqual( myurl.protocol(), 'https')
        self.assertEqual( myurl.domain(), 'www.search.com')
        self.assertEqual( myurl.resource(), '/search?q=zarasa%20bla')

    


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()