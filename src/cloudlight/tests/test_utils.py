'''
Created on Mar 30, 2010

@author: jose
'''
import unittest, time

from cloudlight.utils.misc import Base
from cloudlight.utils.estimator import TimeEstimator

class Test(unittest.TestCase):


    def testNum2Base(self):
        
        base = Base()
        
        self.assertEqual( len(base.alphab), 91 )
        
        self.assertEqual( base.num2base(0), '!' )
        self.assertEqual( base.num2base(45), 'O' )
        self.assertEqual( base.num2base(92), '""' )
        self.assertEqual( base.num2base(100), '"+' )
        self.assertEqual( base.num2base(1000000), '"?g"' )


    def testBase2Num(self):
        
        base = Base()
        
        self.assertEqual( len(base.alphab), 91 )
        
        self.assertEqual( base.base2num('!'), 0 )
        self.assertEqual( base.base2num('O'), 45 ) 
        self.assertEqual( base.base2num('""'), 92 ) 
        self.assertEqual( base.base2num('"+'), 100 ) 
        self.assertEqual( base.base2num('"?g"'), 1000000 ) 


    def testTimeEstimator(self):

        estimator = TimeEstimator(5)
        
        for _ in range(5):
            time.sleep(1.0)
            estimator.tick()
            
        self.assertAlmostEqual( estimator.time_elapsed(), 5.0, places=1)
        
        self.assertAlmostEqual( estimator.time_per_iteration(), 1.0, places=1)
        
        self.assertAlmostEqual( estimator.time_left(), 0.0, places=1)
        
        self.assertEqual( estimator.log_line(), 'INFO: 5 iterations | 5 total , 5.0 secs (0.1 mins) elapsed | 1.0 secs (0.0 mins) per it. | 0.0 secs (0.0 mins) left')
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()