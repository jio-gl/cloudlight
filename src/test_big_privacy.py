#!/usr/bin/python
from cloudlight import BigGraph
from cloudlight import PrivacyAttackStrategies

from cloudlight.utils.itertools_recipes import izip
from cloudlight.utils.estimator import TimeEstimator


import time, sys, os, random

from multiprocessing import Process, Queue

cache_size_pages = 2**16

filename =  len(sys.argv) > 1 and sys.argv[1] or None 

if not filename:
    filename = '/tesis/lj-10k-test.big_graph'
    #print 'Error: first argument missing, input filename with BigGraph archive!'
    #exit(-1)


outname =  len(sys.argv) > 2 and sys.argv[2] or None

if not outname:
    outname = '/tesis/lj-test.privacy'
    #print 'Error: second argument missing, output filename!'
    #exit(-1)


type =  len(sys.argv) > 3 and sys.argv[3] or None

if not type:
    type = 'no_triangles'
    #print 'INFO: third argument missing, attack type (passive, supernode, triangles or no_degree), assuming passive!'
    #type = 'all' #'test' #'all'    


coverage =  len(sys.argv) > 4 and sys.argv[4] or None

if not coverage: # or not coverage in ['node', 'link','korolova', 'triangle']:
    #coverage = 'link'
    print 'INFO: fourth argument missing, coverage type ("complete node" or "link"), assuming "complete node"!'
    coverage_funcs = ['node'] #,'link','triangle','korolova']
else:
    coverage_funcs = coverage.split(',')

end_cov =  len(sys.argv) > 5 and sys.argv[5] or None

if not end_cov :
    #coverage = 'link'
    print 'INFO: fifth argument missing, coverage end (from 5 to 100), assuming 70!'
    end_cov = 40
else:
    end_cov = int(end_cov)


#coverage_type = coverage

debug = True

lookaheads = [0] #,1,2] #,3]

begin_cov = 5
#end_cov   = 100

coverages = [float(i)/100 for i in range(begin_cov,end_cov+5,5)]

if not type or type == 'passive':
    strats = [
              'start_degree', 
              'start_greedy', 
              'start_crawler', 
              'start_random'
              ]
elif type == 'triangles':
    strats = [
              'start_triangles',
              'start_greedy_triangles',
              'start_crawler_triangles',
              'start_crawler_seen_triangles'
              ]
elif type == 'no_degree':
    strats = [
              'start_crawler_seen_degree',
              'start_crawler_degree_hist',
              'start_crawler_degree_hist_bin_dist',
              'start_crawler_degree_hist_bin_dist_rand',
              ]

elif type == 'all':
    strats = [
              'start_crawler_random', 
              'start_crawler_seen_degree', 
              'start_crawler_degree_hist',
              'start_crawler_degree_hist_bin_dist',
              'start_crawler_degree_aprox_hist_bin_dist',
#              'start_random',
#              'start_degree', 
              #'start_crawler_degree_hist_bin_dist_orderby_triangles',
              #'start_crawler_seen_triangles',
              #'start_crawler_degree_hist_bin_dist_rand',

              ##'start_greedy', 
              #'start_crawler', 
              #'start_triangles',
              ##'start_greedy_triangles',
              #'start_crawler_triangles',
              ]
    

elif type == 'test':
    strats = [
              'start_degree', 
              'start_random',
              #'start_greedy', 
              # BUG!!! Excepcion por None node! 
              # VIENE DE QUE EL GRAFO ES DISCONEXO, POR ESO NEXT_NODE_CRAWLER_UNSEEN_DEGREE DA NONE!!!
              #'start_crawler',               
              #'start_triangles',
              # BUG!!! Loop infinito siempre soborna al mismo nodo! 
              #'start_greedy_triangles',
              # Idem 'start_crawler_triangles',
              #'start_greedy_seen_degree',
              # Bug!!! Excepcion por None node! 'start_crawler_seen_degree', 
              'start_greedy_seen_triangles', 
              #'start_crawler_seen_triangles',
              'start_crawler_degree_hist',
              'start_crawler_degree_hist_bin_dist',
              'start_crawler_degree_hist_bin_dist_rand',
              ]
    

elif type == 'supernode':
    lookaheads = [2,3]
    strats = ['start_supernode_degree', 'start_supernode_greedy', 'start_supernode_crawler', 'start_supernode_random']

else:
    raise Exception('Unsupported set of strategies!! %s' % type)


max_effort_fraction = 0.01


# pruebas

# passive    korolova 100% DONE!
# no_degree  link     100% DONE!
# triangles  triangle 100% DONE!
# triangles2 triangle  70% DONE!


# viejas

# no_degree link     100% DONE!
# no_degree korolova 100% DONE!

# passive   link     100% DONE!
# passive   korolova 100% DONE!

# triangles triangle 90% DONE!
# triangles link     100% DONE!
# triangles korolova 100% DONE!

# no_degree triangle ERROR with start_greedy_seen_degree, no more nodes available, coverage still < 100% :(
# passive   triangle ERROR with start_greedy_seen_degree, no more nodes available, coverage still < 100% :(


def coverage_map(func):
             
    if 'node' == func: 
        return 'node_coverage'
    if 'link' == func: 
        return 'link_coverage'
    if 'korolova' == func or 'complete_node' == func: 
        return 'complete_node_coverage'
    if 'triangle' == func: 
        return 'triangle_coverage'

    raise Exception('bad mapping from converage function to coverage name! %s' % str(func))
    
    

q = Queue()

def run(q, strategy, coverages, coverage_funcs, max_effort):

        estimator = TimeEstimator(len(coverages)*len(coverage_funcs))
        
        coverages = dict( [ (coverage_map(cov_func), coverages)  for cov_func in coverage_funcs]  )

        for cost, coverage, coverage_type in strat(coverages, max_effort):
            #print '%d  %.2f  %s  %d' % (l, coverage, strat_name.replace('crawler','crawlr'), cost)
            if cost >= 0: # not finished yet...
                estimator.tick()
                log_line =  estimator.log_line()
                q.put( '%d  %.7f  %s %s  %d  %f  %s\n' % (l, coverage, coverage_type, strat_name.replace('crawler','crawlr'), cost, float(cost)/graph.number_of_nodes(), log_line) )
            else:
                q.put( 'FINISHED' )


create_dbs = True

if create_dbs:
    for strat_name in strats:
        for l in lookaheads:
    
            new_filename = filename + '.%s.lookahead%d' % (strat_name, l)
            print 'creating BigGraph ' + new_filename
            os.system('cp %s %s' % (filename, new_filename))


print 'choosing random node seed for crawlers...'
graph = BigGraph(filename, cache_size_pages)
node_rand_seed = graph.random_nodes()[0]
del graph
print 'done.  choosed -> %s' % str(node_rand_seed)

processors = len(strats)*len(lookaheads) # 4

out = open(outname,'w')
        
        
processes = []
graphs = []
list_of_strategies = []
results = 0
for strat_name in strats:
    for l in lookaheads:

        new_filename = filename + '.%s.lookahead%d' % (strat_name, l)
        graph = BigGraph(new_filename, cache_size_pages)

        max_effort = graph.number_of_nodes() * max_effort_fraction # 
        
        graph.debug = debug
        graph.input_debug_links = 200000
        graph.output_debug_nodes = 10000
        
        graph.max_links_input = 1*10**8
        graph.max_nodes_analysis = 100000000

        print 'PrivacyAttackStrategies with %s ...' % new_filename
        strategies = PrivacyAttackStrategies(graph, l, coverage_funcs, debug)
        strategies.node_rand_seed = node_rand_seed

        strat = eval('strategies.%s' % strat_name)
        
        p = Process(target=run, args=(q,strat, coverages, coverage_funcs, max_effort))
        p.start()
        processes.append( p )
        graphs.append( graph )
        list_of_strategies.append( strategies )

#        results += len(coverages)*len(coverage_funcs)
#        if len(processes) >= processors: #len(strats)*len(lookaheads):  
#            for _ in range(results):
#                res = q.get()
#                out.write(res)
#                out.flush()
#            map(lambda x: x.join(), processes)
#            processes = []
#            graphs = []
#            list_of_strategies = []
#            results = 0      
            
finished_processes = len(strats)*len(lookaheads)
while finished_processes > 0:
    res = q.get()
    if res != 'FINISHED':
        out.write(res)
        out.flush()
    else:
        finished_processes -= 1 # another process finished
      

out.close()

