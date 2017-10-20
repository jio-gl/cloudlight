#!/usr/bin/python
'''
Created on Jun 7, 2010

@author: jose
'''

#!/usr/bin/python
from cloudlight import BigGraph

import sys

filename =  len(sys.argv) > 1 and sys.argv[1] or None 

debug = True

if not filename:
    print 'Error: first argument missing, input filename with BigGraph archive!'
    exit(-1)

# cache size in 2KB pages (?)
cache_size = 2**16

print 'opening BigGraph ' + filename
graph = BigGraph(filename, cache_size)
graph.debug = debug

print 'indexing with create_index_kcores()' 
graph.create_index_kcores()

