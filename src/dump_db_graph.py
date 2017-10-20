#!/usr/bin/python
'''
Created on Jul 20, 2010

@author: jose
'''

from cloudlight import BigGraph

import sys

print sys.argv

filename =  len(sys.argv) > 1 and sys.argv[1] or None 

if not filename:
    #filename = 'orkut-links-fst.txt.toundirected.30mill'
    print 'Error: first argument missing, input filename with space separated graph!'
    exit(-1)

outname =  len(sys.argv) > 2 and sys.argv[2] or None

if not outname:
    #outname = 'orkut-2k_sym.big_graph'
    print 'Error: second argument missing, output filename!'
    exit(-1)

graphfile = filename

graph = BigGraph(graphfile)

graph.debug = True
graph.input_debug_links = 200000
graph.output_debug_nodes = 10000

print 'NODES:'
print graph.number_of_nodes()
print 'EDGES:'
print graph.number_of_edges()
print 'dumping Graph to edge list file ...'
graph.save_edgelist(outname)
print 'done.'




