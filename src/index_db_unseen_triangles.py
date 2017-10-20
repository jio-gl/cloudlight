#!/usr/bin/python
'''
Created on May 23, 2010

@author: jose
'''

from cloudlight import BigGraph

import sys

filename =  len(sys.argv) > 1 and sys.argv[1] or None 

if not filename:
    print 'Error: first argument missing, input filename with BigGraph archive!'
    exit(-1)

print 'opening BigGraph ' + filename
graph = BigGraph(filename)

print 'indexing with create_index_unseen_triangles()'
graph.index_parameter_from_parameter('triangles', 'unseen_triangles')



if __name__ == '__main__':
    pass