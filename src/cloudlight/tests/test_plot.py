'''
Created on Mar 29, 2010

@author: jose
'''
import unittest
from cStringIO import StringIO

from cloudlight.algorithms.plot import Plot
from cloudlight.classes.graph import Graph
from cloudlight.tests.data import example_txt, example_txt2
 


class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testBasicHistogram(self):
        x = map(lambda x : 2**x , range(0,5) )    
        p = Plot()
        p.clear()    
        p.hist( x, 4, False, False, False )
        #p.show()
        

    def testGraphHistogram(self):
        self.graph = Graph()
        self.graph.debug = False
        self.graph.input_debug_links = 200000
        self.graph.output_debug_nodes = 10000
        self.graph.load_edgelist(StringIO(example_txt2))

        degrees = list(self.graph.degrees())        
        p = Plot()    
        p.clear()    
        p.hist( degrees, 15, True, True, False )
        #p.show()

        
    def testPlotSave(self):
        self.graph = Graph()
        self.graph.debug = False
        self.graph.input_debug_links = 200000
        self.graph.output_debug_nodes = 10000
        self.graph.load_edgelist(StringIO(example_txt))

        clusts = list( self.graph.eccentricities() )
        clusts
        p = Plot()    
        p.clear()    
        p.hist( clusts, 3, True, True, True )
        p.save('testPlotSave.png')
        #p.show()
        
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()