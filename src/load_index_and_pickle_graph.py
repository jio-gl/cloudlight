#!/usr/bin/python
'''
Created on Jul 20, 2010

@author: jose
'''

from cloudlight import Graph

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

links =  len(sys.argv) > 3 and sys.argv[3] or None

if not links:
    #links = 2000
    print 'Error: third argument missing, max number of links!'
    exit(-1)
else:
    links = int(links)


graph = Graph()

graph.debug = True
graph.input_debug_links = 200000
graph.output_debug_nodes = 10000

graph.max_links_input = links
graph.max_nodes_analysis = 1000000000

graph.load_index_and_pickle(open(filename), True, outname)


