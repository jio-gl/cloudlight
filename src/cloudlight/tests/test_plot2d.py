'''
Created on Apr 19, 2010

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


    def testPlot2D(self):
        x = range(0,5) + [1]
        y = map(lambda x : 2**x , range(0,5) ) + [3]    
        p = Plot()
        p.clear()    
        p.dist_plot_2d(x, y, 5, False )
        #p.show()


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()