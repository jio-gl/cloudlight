#!/usr/bin/python
'''
Created on Jun 30, 2010

@author: jose
'''

from cloudlight import BigGraph

import sys

print sys.argv

filename =  len(sys.argv) > 1 and sys.argv[1] or None 

if not filename:
    print 'Error: first argument missing, input filename with BigGraph archive!'
    exit(-1)

# cache size in 2KB pages (?)
cache_size = 2**18

print 'opening BigGraph ' + filename
graph = BigGraph(filename, cache_size)

    

print 'indexing with create_index_degree()'
graph.create_index_degree()

print 'indexing with create_index_knn()' 
graph.create_index_knn()

print 'indexing with create_index_clustering()'
graph.create_index_clustering()
    
print 'indexing with create_index_kcores()' 
graph.create_index_kcores()

print 'indexing with create_index_triangles()' 
graph.create_index_triangles()

#for lookahead in [1,2,3]:
for lookahead in [1]:
    
    print 'indexing with create_index_nodesphere( lookahead  = %d)' % lookahead
    graph.create_index_nodesphere(lookahead)

    print 'indexing with create_index_linksphere( lookahead  = %d)' % lookahead
    graph.create_index_linksphere(lookahead)
            
                
        

