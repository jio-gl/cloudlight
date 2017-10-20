'''
Created on Apr 8, 2010

@author: jose
'''

from cloudlight.classes.graph import Graph
from cloudlight.algorithms.plot import Plot


g = Graph()

g.max_links_input = 50000

g.load_edgelist(open('orkut-links-fst.txt.toundirected.3mill'), num=True )

g.save_compressed_graph('./cloudlight/tests/data_enc1.py', False)
g.save_compressed_graph('./cloudlight/tests/data_enc2.py', True)


