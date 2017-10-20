#!/usr/bin/python
'''
Created on Jul 30, 2010

@author: jose
'''
from cloudlight import BigGraph

import sys

filename =  len(sys.argv) > 1 and sys.argv[1] or None 

if not filename:
    print 'Error: first argument missing, input filename with BigGraph archive!'

print 'opening BigGraph ' + filename
graph = BigGraph(filename)

print 'dropping index with remove_parameter_cache()'
graph.remove_parameter_cache('seen_triangles')



if __name__ == '__main__':
    pass
