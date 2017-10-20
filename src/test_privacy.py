#!/usr/bin/python
'''
Created on Jul 21, 2010

@author: jose
'''

from cloudlight import Graph
from cloudlight import PrivacyAttackStrategies

from cloudlight.utils.itertools_recipes import izip
from cloudlight.utils.estimator import TimeEstimator


import time, sys, os, cPickle

usage = '''
Usage: %s pickled-graph-filename experiment-results-outfilename attack-type
            
            attack-type : can be "passive" or "supernode"  
''' % sys.argv[0] 

filename =  len(sys.argv) > 1 and sys.argv[1] or None 

if not filename:
    print 'Error: first argument missing, input filename with Graph pickle file!'
    print usage
    exit(-1)


outname =  len(sys.argv) > 2 and sys.argv[2] or None

if not outname:
    #outname = '/tesis/flickr-growth.txt-200k.big_graph.passive'
    print 'Error: second argument missing, output filename!'
    print usage
    exit(-1)


type =  len(sys.argv) > 3 and sys.argv[3] or None

if not type:
    print 'INFO: third argument missing, attack type (passive, supernode or ...), assuming passive!'
    type = 'passive'

coverage =  len(sys.argv) > 4 and sys.argv[4] or None

if not coverage or not coverage in ['node','link','korolova', 'triangle']:
    print 'INFO: fourth argument missing, coverage type ("complete node" or "link"), assuming "complete node"!'
    coverage = 'complete node'


debug = True

coverage_type = coverage
lookaheads = [1,2,3]

begin_cov = 5
end_cov   = 90

coverages = [float(i)/100 for i in range(begin_cov,end_cov+5,5)]

if not type or type == 'passive':
    strats = ['start_degree', 'start_greedy', 'start_crawler', 'start_random']
elif type == 'supernode':
    lookaheads = [2,3]
    strats = ['start_supernode_degree', 'start_supernode_greedy', 'start_supernode_crawler', 'start_supernode_random']
elif type == 'triangles':
    strats = ['start_triangles', 'start_greedy_triangles', 'start_crawler_triangles', 'start_random']


def run(out, strategy, coverages, max_effort):

        estimator = TimeEstimator(len(coverages))
        for coverage, cost in izip(iter(coverages), strat(coverages, max_effort)):
            #print '%d  %.2f  %s  %d' % (l, coverage, strat_name.replace('crawler','crawlr'), cost)
            estimator.tick()
            log_line =  estimator.log_line()
            out.write( '%d  %.2f  %s  %d  %f  %s\n' % (l, coverage, strat_name.replace('crawler','crawlr'), cost, float(cost)/graph.number_of_nodes(), log_line) )


#print 'loading Graph pickled from %s ...' % filename
#graph = cPickle.load(open(filename))

graph = Graph()

graph.debug = debug
graph.input_debug_links = 200000
graph.output_debug_nodes = 10000

graph.max_links_input = 1*10**8
graph.max_nodes_analysis = 100000000

graph.load_edgelist(open(filename), True, False)
graph.create_index_degree()
graph.create_index_triangles()

out = open(outname,'w')
        
for strat_name in strats:
    for l in lookaheads:

        new_filename = filename + '.%s.lookahead%d' % (strat_name, l)

        max_effort = graph.number_of_nodes()
        
        graph.reset_edge_weights()
        
        if coverage_type == 'complete node' or 'start_crawler' == strat_name or 'start_greedy' == strat_name:
            try:
                graph.remove_parameter_cache('unseen_degree')
            except:
                pass
            graph.index_parameter_from_degree('unseen_degree')

        if 'triangle' in strat_name: # or 'triangle' in coverage_type:
            try:
                graph.remove_parameter_cache('unseen_triangles')
            except:
                pass
            graph.index_parameter_from_parameter('triangles', 'unseen_triangles')

        if 'triangle' == coverage_type: # or 'triangle' in coverage_type:
            try:
                graph.remove_parameter_cache('seen_triangles')
                graph.remove_parameter_cache('seen_triangles2')
            except:
                pass
            graph.add_parameter_cache('seen_triangles')
            graph.initialize_parameter('seen_triangles', 0.0)
            graph.index_parameter_cache('seen_triangles')
            graph.add_parameter_cache('seen_triangles2')
            graph.initialize_parameter('seen_triangles2', 0.0)
            graph.index_parameter_cache('seen_triangles2')

        print 'PrivacyAttackStrategies with %s ...' % new_filename
        strategies = PrivacyAttackStrategies(graph, l, coverage_type, debug)

        strat = eval('strategies.%s' % strat_name)
        
        run(out, strat, coverages, max_effort)
            

out.close()

