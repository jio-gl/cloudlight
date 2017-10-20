'''
Created on Apr 9, 2010

@author: jose
'''


import random



class Node(object):
    
    def __init__(self):
        
        self.id = str(random.random())

    def __repr__(self):
        
        return self.id
