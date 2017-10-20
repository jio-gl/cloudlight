'''
Created on Mar 27, 2010

@author: jose
'''
import unittest
from cStringIO import StringIO

from cloudlight.classes.graph import Graph
from cloudlight.tests.data import example_txt
from cloudlight.bots.io import Printer
from cloudlight.bots.traversal import DFSBot, BFSBot


class Test(unittest.TestCase):


    def setUp(self):
        self.graph = Graph()
        self.graph.debug = False
        self.graph.input_debug_links = 1
        self.graph.output_debug_nodes = 1
        self.graph.load_edgelist(StringIO(example_txt), num=True)


    def tearDown(self):
        pass


    def testPrinter(self):
        printer = Printer()
        result = '\n'.join( printer.visit(self.graph) )
        self.assertEqual( result, 'NODE: 1\nNODE: 2\nNODE: 3\nNODE: 4\nNODE: 5\nNODE: 6\nNODE: 7\nNODE: 8\nNODE: 9\nNODE: 666\nEDGE: 1 -- 2 ATTRS: \nEDGE: 3 -- 5 ATTRS: \nEDGE: 4 -- 5 ATTRS: \nEDGE: 6 -- 7 ATTRS: \nEDGE: 7 -- 8 ATTRS: \nEDGE: 7 -- 9 ATTRS: \nEDGE: 8 -- 9 ATTRS: \nEDGE: 9 -- 666 ATTRS: ' )
        

    def testDFSBot(self):
        bot = Printer(None, DFSBot())
        result = '\n'.join( bot.visit(self.graph) )
        self.assertEqual( result, 'NODE: 666\nEDGE: 666 -- 9 ATTRS: \nNODE: 9\nEDGE: 9 -- 8 ATTRS: \nEDGE: 9 -- 666 ATTRS: \nEDGE: 9 -- 7 ATTRS: \nNODE: 7\nEDGE: 7 -- 8 ATTRS: \nEDGE: 7 -- 9 ATTRS: \nEDGE: 7 -- 6 ATTRS: \nNODE: 6\nEDGE: 6 -- 7 ATTRS: \nNODE: 8\nEDGE: 8 -- 9 ATTRS: \nEDGE: 8 -- 7 ATTRS: \nNODE: 8\nEDGE: 8 -- 9 ATTRS: \nEDGE: 8 -- 7 ATTRS: ' )


    def testBFSBot(self):
        bot = Printer(None, BFSBot())
        result = '\n'.join( bot.visit(self.graph) )
        self.assertEqual( result, 'NODE: 666\nEDGE: 666 -- 9 ATTRS: \nNODE: 9\nEDGE: 9 -- 8 ATTRS: \nEDGE: 9 -- 666 ATTRS: \nEDGE: 9 -- 7 ATTRS: \nNODE: 8\nEDGE: 8 -- 9 ATTRS: \nEDGE: 8 -- 7 ATTRS: \nNODE: 7\nEDGE: 7 -- 8 ATTRS: \nEDGE: 7 -- 9 ATTRS: \nEDGE: 7 -- 6 ATTRS: \nNODE: 7\nEDGE: 7 -- 8 ATTRS: \nEDGE: 7 -- 9 ATTRS: \nEDGE: 7 -- 6 ATTRS: \nNODE: 6\nEDGE: 6 -- 7 ATTRS: \nNODE: 6\nEDGE: 6 -- 7 ATTRS: ' )


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()