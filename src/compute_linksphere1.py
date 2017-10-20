#!/usr/bin/python
'''
Created on May 27, 2010

@author: jose
'''

from cloudlight import izip

import sys, os

folder =  len(sys.argv) > 1 and sys.argv[1] or None 

if not folder:
    print 'Error: first argument missing, input folder with BigGraph parameters!'


degrees = open(os.path.abspath(folder)+'/degree.txt')
clusts = open(os.path.abspath(folder)+'/clustering.txt')
knns = open(os.path.abspath(folder)+'/knn.txt')

out = open(os.path.abspath(folder)+'/linksphere1.txt.equation', 'w')
count = 0
for (d,c),k in izip(izip(degrees,clusts),knns):    
    
    d, c, k = float(d), float(c), float(k)
    if count % 10000 == 0:
        print 'INFO: computing linksphere1 %d nodes ...' % (count)
        
    value = ( k - c * (d-1)/2 ) * d
    out.write('%f\n' % (value) )
    
    count += 1

out.close()
