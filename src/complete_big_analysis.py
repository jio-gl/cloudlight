#!/usr/bin/python
'''
Created on May 28, 2010

@author: jose
'''
import sys

from cloudlight.classes.big_graph import BigGraph
from cloudlight.algorithms.plot import Plot


filename =  len(sys.argv) > 1 and sys.argv[1] or None 

if not filename:
    #filename = '/tesis/flickr-growth.txt-200k.big_graph' 
    print 'Error: first argument missing, input filename with space separated graph!'
    exit(-1)

graph = BigGraph(filename)

debug = True

graph.debug = debug
#graph.input_debug_links = 200000
graph.output_debug_nodes = 10000

#graph.max_links_input = 5*10**4
#graph.max_nodes_analysis = 10000


folder =  len(sys.argv) > 2 and sys.argv[2] or None 

if not folder:
    #folder = '/tesis/flickr-growth.txt-200k.big_graph.analysis'
    print 'Error: second argument missing, output folder name!'
    exit(-1)

user_params =  len(sys.argv) > 3 and sys.argv[3] or None 

if not user_params:
    user_params = 'degree,clustering,knn'

p = Plot(debug)

sample_size = graph.number_of_nodes()
bins = 8
compute_data = True

params = {
                  'degree' : 10, #17,
                  'clustering' : 10,#15,
                  'knn' : 10,#12,
                  'kcore' : 10,#10,
                  'triangles' : 10,
                  'linksphere1' : 10,
                  #'linksphere2' : 10,
                  #'linksphere3' : 10,
                  'nodesphere1' : 10,
                  #'nodesphere2' : 10,
                  #'nodesphere3' : 10,
                  #'eccentricity' : 10,#15,
                  #'path_len' : 15,#30,
                  #'scaling' : 8,#10,
                  #'connectivity' : 8,#10,
                  }

params = dict([(param,params[param]) for param in user_params.split(',')])

p.init_complete_analysis(graph, folder, sample_size, bins, 666, params )
if compute_data:
    p.complete_analysis(graph)
p.plot_graph_params()    
