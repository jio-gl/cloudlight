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
    exit(-1)

print 'opening BigGraph ' + filename
graph = BigGraph(filename)

print 'indexing with create_index_seen_triangles()'
graph.add_parameter_cache('seen_triangles')
graph.initialize_parameter('seen_triangles', 0.0)
graph.index_parameter_cache('seen_triangles')
graph.add_parameter_cache('seen_triangles2')
graph.initialize_parameter('seen_triangles2', 0.0)
graph.index_parameter_cache('seen_triangles2')



if __name__ == '__main__':
    pass