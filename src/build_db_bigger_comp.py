#!/usr/bin/python
'''
Created on Aug 1, 2010

@author: jose
'''

from cloudlight import BigGraph, Graph

import networkx as nx
import sys

print sys.argv

filename =  len(sys.argv) > 1 and sys.argv[1] or None 

if not filename:
    print 'Error: first argument missing, input filename with BigGraph!'
    exit(-1)

outname =  len(sys.argv) > 2 and sys.argv[2] or None

if not outname:
    print 'Error: second argument missing, output filename for BigGraph!'
    exit(-1)



graph = BigGraph(filename)
#graph = BigGraph()

#graph.add_edge(1,2)
#graph.add_edge(2,3)
#graph.add_edge(3,1)

#graph.add_edge(4,5)

aux_graph = Graph()
connected_graph = BigGraph(outname)

graph.add_random_component(aux_graph)

for src,dst in aux_graph.edges_iter():
    connected_graph.add_edge(src,dst)

connected_graph.create_indices()

print 'input Graph:'
print 'nodes = %d' % graph.number_of_nodes()
print 'edges = %d' % graph.number_of_edges()

print 'output connected Graph:'
print 'nodes = %d' % connected_graph.number_of_nodes()
print 'edges = %d' % connected_graph.number_of_edges()



