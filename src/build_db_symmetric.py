#!/usr/bin/python
'''
Created on Apr 28, 2010

@author: jose
'''

from cloudlight import BigDiGraph, BigGraph

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

graphfile = outname

digraph = BigDiGraph(graphfile+'.big_digraph')

digraph.debug = True
digraph.input_debug_links = 200000
digraph.output_debug_nodes = 100

digraph.max_links_input = links
digraph.max_nodes_analysis = 10000

print 'digraph.load_edgelist(open(filename)) ...'
digraph.load_edgelist(open(filename))

print 'digraph.create_indices() ...'
digraph.create_indices()

graph = BigGraph(graphfile+'.disconnected')

print 'digraph.add_only_symmetric_edgelist(graph) ...'
digraph.add_only_symmetric_edgelist(graph)

print 'graph.create_indices() ...'
graph.create_indices()

number_of_nodes = graph.number_of_nodes()
comps = [ len(comp)/float(number_of_nodes)  for comp in graph.connected_components() ]

if comps[0] < 0.5:
    print 'ERROR: biggest connected componnet not found!'
    exit(-1)
    

print 'input DiGraph:'
print 'nodes = %d' % digraph.number_of_nodes()
print 'edges = %d' % digraph.number_of_edges()

print 'output Graph (possibly disconnected):'
print 'nodes = %d' % graph.number_of_nodes()
print 'edges = %d' % graph.number_of_edges()
print 'connected components fractions: %s' % str(comps)

digraph.erase_from_disk()


