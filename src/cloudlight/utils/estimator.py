'''
Created on Jun 30, 2010

@author: jose
'''

import time, datetime

class TimeEstimator(object):
    '''
    A class for estimating finish time of iterations.
    '''


    def __init__(self, total_ticks):
        '''
        Constructor
        '''
        
        self.__total_ticks = total_ticks        
        self.__ticks = 0
        self.__init_time = time.time()    
        
        
    def tick(self):
        
        self.__ticks += 1
        
        
    def time_elapsed(self):
        
        return time.time() - self.__init_time

    
    def time_per_iteration(self):
        
        return self.time_elapsed() / self.__ticks
    
    
    def time_left(self):
        
        return self.time_per_iteration() * (self.__total_ticks - self.__ticks)
    
        
    def log_line(self):
        
	end_time = (datetime.datetime.today() + datetime.timedelta(0,self.time_left())).ctime()

        est_vars = (time.ctime(), self.__ticks, self.__total_ticks, self.time_elapsed(), self.time_elapsed()/60, self.time_per_iteration(), self.time_per_iteration()/60, self.time_left(), self.time_left()/60, end_time)

        return '(%s) %d its. | %d total , %.1f secs (%.1f mins) elapsed | %.1f secs (%.1f mins) per it. | %.1f secs (%.1f mins) left (ending %s)' % est_vars
    
        
        
