#!/usr/bin/python
'''
Created on Jun 29, 2010

@author: jose
'''

from cloudlight import BigGraph

import sys

filename =  len(sys.argv) > 1 and sys.argv[1] or None 

if not filename:
    print 'Error: first argument missing, input filename with BigGraph archive!'
    exit(-1)

type =  len(sys.argv) > 2 and sys.argv[2] or None 

if type != 'node' and type != 'link':
    print 'Error: second argument missing, input sphere type (link o node)!'
    exit(-1)

lookahead =  len(sys.argv) > 3 and int(sys.argv[3]) or None 

if not lookahead:
    print 'Error: third argument missing, input sphere lookahead (radius minus one)! lookahead 0 (zero) equals degree...'
    exit(-1)

outname =  len(sys.argv) > 4 and sys.argv[4] or None

if not outname:
    #outname = '/tesis/flickr-growth.txt-200k.big_graph.passive'
    print 'Error: second argument missing, output filename!'
    exit(-1)

print 'opening BigGraph ' + filename
graph = BigGraph(filename)


out = open(outname, 'w')

total_nodes = graph.number_of_nodes()
count = 0
for node, clustering in graph.get_parameter_cache_iter('%ssphere%d' % (type, lookahead) ) :
    
    
    if count % 10000 == 0:
        print 'INFO: exporting clustering %d nodes of %d total nodes' % (count, total_nodes)
        
    out.write('%s\t\t%f\n' % (node, clustering) )
    
    count += 1


