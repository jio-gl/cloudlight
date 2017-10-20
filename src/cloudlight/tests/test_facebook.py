'''
Created on Mar 23, 2010

@author: jose
'''

import unittest

from cloudlight.nodes.facebook import FacebookNode


class Test(unittest.TestCase):


    def setUp(self):
        FacebookNode.initialize({}, 'alice.private.life@gmail.com', 'asdfasdf0', False)
        #FacebookNode.initialize({}, 'bob.private.life@gmail.com', 'asdfasdf0', False)


    def tearDown(self):
        pass


    def testFacebook1(self):

        self.node = FacebookNode(1151613578)
        self.assertEqual(self.node.id, 1151613578)
        self.node.grab_user_details()
        self.assertEqual(self.node.name, 'Gerardo Richarte')
        friends = self.node.friends()
        self.assertEqual(len(friends[:100]), 100)
        self.assertEqual(friends[0].id, 507271730)



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()