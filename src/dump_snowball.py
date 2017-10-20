#!/usr/bin/python
'''
Created on Oct 4, 2010

@author: jose
'''

from cloudlight import BigGraph

import sys

if __name__ == '__main__':
    
    print 'Starting dump_snowball'
    
    filename =  len(sys.argv) > 1 and sys.argv[1] or None 
    
    if not filename:
        print 'Error: first argument missing, input filename with BigGraph archive!'
        exit(-1)
    
    
    outname =  len(sys.argv) > 2 and sys.argv[2] or None
    
    if not outname:
        print 'Error: first argument missing, output filename with edgelist archive!'
        exit(-1)
    
    g = BigGraph(filename)
    g.debug = True
    g.save_snowball_edgelist_iter(outname)
    