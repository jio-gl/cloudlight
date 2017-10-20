#!/usr/bin/python


import sys

from cloudlight.classes.graph import Graph
from cloudlight.algorithms.plot import Plot
import cloudlight.tests.data_enc1

graph = Graph()

graph.debug = True
graph.input_debug_links = 200000
graph.output_debug_nodes = 100

graph.max_links_input = 5*10**7
graph.max_nodes_analysis = 10000

filename =  len(sys.argv) > 1 and sys.argv[1] or None 

filename = '/media/truecrypt1/temp/livejournal-links.txt-symmetric.snowball.10k'

if not filename:
    print 'Error: first argument missing, input filename with space separated graph!'
    exit(-1)

folder =  len(sys.argv) > 2 and sys.argv[2] or None 

folder = '/media/truecrypt1/temp/lj/'

if not folder:
    print 'Error: second argument missing, output folder name!'
    exit(-1)
            
user_params =  len(sys.argv) > 3 and sys.argv[3] or None 

if not user_params:
    user_params = 'degree,clustering,knn'


graph.load_edgelist(open(filename), num=True)
graph.create_index_degree()

p = Plot()

p.debug = True
sample_size = 1000
bins = 8
compute_data = True

params = {
                  'degree' : 10, #17,
                  'clustering' : 10,#15,
                  'knn' : 10,#12,
                  'kcore' : 5,#10,
                  'eccentricity' : 10,#15,
                  'path_len' : 15,#30,
                  'scaling' : 8,#10,
                  'connectivity' : 8,#10,
                  }

params = dict([(param,params[param]) for param in user_params.split(',')])

p.init_complete_analysis(graph, folder, sample_size, bins, 666, params )
if compute_data:
    p.complete_analysis(graph)
p.plot_graph_params()    
