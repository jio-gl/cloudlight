#!/usr/bin/python
'''
Created on May 27, 2010

@author: jose
'''

from cloudlight import BigGraph

import sys

filename =  len(sys.argv) > 1 and sys.argv[1] or None 

if not filename:
    print 'Error: first argument missing, input filename with BigGraph archive!'

print 'opening BigGraph ' + filename
graph = BigGraph(filename)

print 'nodes: %d' % graph.number_of_nodes()
print 'edges: %d' % graph.number_of_edges()

