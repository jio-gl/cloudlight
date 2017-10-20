#!/usr/bin/python
'''
Created on May 13, 2010

@author: jose
'''

from cloudlight import BigDiGraph

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


digraph = BigDiGraph(outname)

digraph.debug = True
digraph.input_debug_links = 200000
digraph.output_debug_nodes = 10000

digraph.max_links_input = links
digraph.max_nodes_analysis = 1000000000

digraph.load_edgelist(open(filename))

digraph.create_indices()

print 'input DiGraph:'
print 'nodes = %d' % digraph.number_of_nodes()
print 'edges = %d' % digraph.number_of_edges()

