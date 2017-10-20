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

outname =  len(sys.argv) > 2 and sys.argv[2] or None

if not outname:
    #outname = '/tesis/flickr-growth.txt-200k.big_graph.passive'
    print 'Error: second argument missing, output filename!'
    exit(-1)

print 'opening BigGraph ' + filename
graph = BigGraph(filename)


out = open(outname, 'w')

total_nodes = graph.number_of_nodes()
count = 0
for node, degree in graph.get_parameter_cache_iter('degree'):
    
    
    if count % 10000 == 0:
        print 'INFO: exporting degree %d nodes of %d total nodes' % (count, total_nodes)
        
    out.write('%s\t\t%f\n' % (node, degree) )
    
    count += 1


