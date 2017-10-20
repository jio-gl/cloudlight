'''
Created on May 10, 2010

@author: jose
'''

from cloudlight.algorithms.privacy import LinkPrivacyModel

import random


class PrivacyAttackStrategiesException(Exception):
    '''
    classdocs
    '''
    pass



class PrivacyAttackStrategies(object):
    '''
    Different attack strategies to target LinkPrivacyModels
    '''
    
    def __init__(self, graph, lookahead, coverage_funcs=['node'], debug=True):
        '''
        graph : graph where the attack take place
        looakead : integer measuring the visibility of the nodes
        coverage_func : choose "node" for default node_coverage or "link" for link_coverage of the attack
        '''
        
        self.model = LinkPrivacyModel(graph, lookahead, debug)
            
        self.debug = debug
        
        self.node_rand_seed = None
      
        self.coverage_types = coverage_funcs
        self.model.coverage_types = coverage_funcs
        self.coverage_functions = []

        if 'node' in coverage_funcs :
            self.coverage_functions.append( (self.model.node_coverage, 'node_coverage') )
        if 'link' in coverage_funcs:
            self.coverage_functions.append( (self.model.link_coverage, 'link_coverage') )
        if 'triangle' in coverage_funcs:
            self.coverage_functions.append( (self.model.triangle_coverage, 'triangle_coverage') )
        if 'complete_node' in coverage_funcs or 'korolova' in coverage_funcs :
            self.coverage_functions.append( (self.model.korolova_node_coverage, 'complete_node_coverage') )
            

    def start_node_order(self, coverages={'node':[0.05,0.10],'link':[0.05,0.10]}, max_effort=None, nlist=[], name=None):        

        if len(coverages) < 1:
            raise PrivacyAttackStrategiesException('Error: strategies need a non-empty listo of graph float coverages!')

        for node in nlist:

            if self.debug:
                print 'bribing node... %s -> %s' % (str(name),node)
                print 'lookahead %d' % self.model.lookahead

            self.model.add_bribed_node(node)

            if self.debug:
                print 'effort: %d' % self.model.total_effort()
            
            for cov_func, cov_func_name in self.coverage_functions:
                
                if not cov_func_name in coverages:
                    continue
                
                cov = cov_func()
                
                if self.debug:
                    print 'coverage %s: ' % (cov_func_name)
                    print '             %f' % (cov)

                yield self.model.total_effort(), cov, cov_func_name

            if self.model.total_effort() >= max_effort:
                break
            
        # finish signal!
        yield -1, None, None
        

    def start_degree(self, coverages=[0.20], max_effort=999999999):

        self.model.strategy = 'start_degree'
        for effort, coverage_frac, coverage_type in self.start_node_order(coverages, max_effort, self.model.sorted_degrees_dec_iter(), 'start_degree'):
            yield effort, coverage_frac, coverage_type


    def start_triangles(self, coverages=[0.20], max_effort=999999999):

        self.model.strategy = 'start_triangles'
        for effort, coverage_frac, coverage_type in self.start_node_order(coverages, max_effort, self.model.sorted_triangles_dec_iter(), 'start_triangles'):
            yield effort, coverage_frac, coverage_type


    def start_random(self, coverages=[0.20], max_effort=999999999):
        
        self.model.strategy = 'start_random'
        for effort, coverage_frac, coverage_type in self.start_node_order(coverages, max_effort, self.model.random_node_order_iter(), 'start_random'):
            yield effort, coverage_frac, coverage_type


    def start_next_node(self, coverages=[0.20], max_effort=None, next_func=None):        

        prev_node = None

        if len(coverages) < 1:
            raise PrivacyAttackStrategiesException('Error: strategies need a non-empty listo of graph float coverages!')

        nc = 0
        while nc < self.model.graph.number_of_nodes():
            
            node = next_func()
            
            if node == None or (prev_node and node == prev_node):
                break
            else:
                prev_node = node
            
            if self.debug:
                print 'bribing node... %s -> %s' % (str(next_func),node)
                print 'lookahead %d' % self.model.lookahead
                                
            self.model.add_bribed_node(node)

            if self.debug:
                print 'effort: %d' % self.model.total_effort()
            
            for cov_func, cov_func_name in self.coverage_functions:
                
                if not cov_func_name in coverages:
                    continue

                cov = cov_func()
                
                if self.debug:
                    print 'coverage %s: ' % (cov_func_name)
                    print '             %f' % (cov)
    
                yield self.model.total_effort(), cov, cov_func_name

            if self.model.total_effort() >= max_effort:
                break
            
            nc += 1

        # finish signal!
        yield -1, None, None
            

    def start_greedy(self, coverages=[0.20], max_effort=999999999):
        self.model.strategy = 'start_greedy'
        return self.start_next_node(coverages, max_effort, self.model.max_unseen_degree_node)


    def start_greedy_triangles(self, coverages=[0.20], max_effort=999999999):
        self.model.strategy = 'start_greedy_triangles'
        return self.start_next_node(coverages, max_effort, self.model.max_unseen_triangles_node)


    def start_greedy_seen_degree(self, coverages=[0.20], max_effort=999999999):
        self.model.strategy = 'start_greedy_seen_degree'
        return self.start_next_node(coverages, max_effort, self.model.max_seen_degree_node)


    def start_greedy_seen_triangles(self, coverages=[0.20], max_effort=999999999):
        self.model.strategy = 'start_greedy_seen_triangles'
        return self.start_next_node(coverages, max_effort, self.model.max_seen_triangles_node)


    def start_crawler(self, coverages=[0.20], max_effort=999999999):

        self.model.strategy = 'start_crawler'

        return ( self.start_crawler_generic(coverages, max_effort, self.model.max_unseen_degree_crawler_node) )
                    
        
    def start_crawler_triangles(self, coverages=[0.20], max_effort=999999999):

        self.model.strategy = 'start_crawler_triangles'

        return ( self.start_crawler_generic(coverages, max_effort, self.model.max_unseen_triangles_crawler_node) )


    def start_crawler_seen_degree(self, coverages=[0.20], max_effort=999999999):

        self.model.strategy = 'start_crawler_seen_degree'

        return ( self.start_crawler_generic(coverages, max_effort, self.model.max_seen_degree_crawler_node) )

        
    def start_crawler_random(self, coverages=[0.20], max_effort=999999999):

        self.model.strategy = 'start_crawler_random'

        return ( self.start_crawler_generic(coverages, max_effort, self.model.random_crawler_node) )

        
    def start_crawler_seen_triangles(self, coverages=[0.20], max_effort=999999999):

        self.model.strategy = 'start_crawler_seen_triangles'

        return ( self.start_crawler_generic(coverages, max_effort, self.model.max_seen_triangles_crawler_node) )

        
    def start_crawler_degree_hist(self, coverages=[0.20], max_effort=999999999):

        self.model.strategy = 'start_crawler_degree_hist'

        self.model.initialize_histogram_degree()

        next_node = self.model.histogram_degree_crawler_node
        return ( self.start_crawler_generic(coverages, max_effort, next_node) )

        
    def start_crawler_degree_hist_bin_dist(self, coverages=[0.20], max_effort=999999999):

        self.model.strategy = 'start_crawler_degree_hist_bin_dist'

        self.model.initialize_histogram_degree()

        next_node = self.model.histogram_degree_crawler_node_bin_dist
        return ( self.start_crawler_generic(coverages, max_effort, next_node) )

        
    def start_crawler_degree_aprox_hist_bin_dist(self, coverages=[0.20], max_effort=999999999):

        self.model.strategy = 'start_crawler_degree_aprox_hist_bin_dist'

        deg_dist = lambda deg : 0.844 * deg**-1.844 # TODO
        self.model.initialize_histogram_degree_dist(degree_dist=deg_dist, number_of_nodes=self.model.number_of_nodes)

        next_node = self.model.histogram_degree_crawler_node_bin_dist
        return ( self.start_crawler_generic(coverages, max_effort, next_node) )

        
    def start_crawler_degree_hist_bin_dist_orderby_triangles(self, coverages=[0.20], max_effort=999999999):

        self.model.strategy = 'start_crawler_degree_hist_bin_dist_orderby_triangles'

        self.model.initialize_histogram_degree()

        next_node = self.model.histogram_degree_crawler_node_bin_dist_orderby_triangles
        return ( self.start_crawler_generic(coverages, max_effort, next_node) )

        
    def start_crawler_degree_hist_bin_dist_rand(self, coverages=[0.20], max_effort=999999999):

        self.model.strategy = 'start_crawler_degree_hist_bin_dist_rand'

        self.model.initialize_histogram_degree()

        next_node = self.model.histogram_degree_crawler_node_bin_dist_rand
        return ( self.start_crawler_generic(coverages, max_effort, next_node) )

        
    def start_crawler_generic(self, coverages=[0.20], max_effort=999999999, next_func=None):
        
        # use the same seed of choose random node to start crawling...
        if self.node_rand_seed:
            node = self.node_rand_seed
        else:
            raise Exception('NOOOOOOOOOO')
            node = None
            for n in self.model.random_node_order_iter():
                node = n
                break
        #node = self.model.random_node()

        if self.debug:
            print 'bribing node... %s -> %s' % (str(next_func),node)
            print 'lookahead %d' % self.model.lookahead
        
        print 'FIRST BRIBED NODE! -> ', node, 'degree=', self.model.graph.degree(node), 'neighbors=', str(list(self.model.graph.neighbors_iter(node)))
        
        # first node to bribe 
        self.model.add_bribed_node(node)

        if self.debug:
            print 'effort: %d' % self.model.total_effort()
        
        for cov_func, cov_func_name in self.coverage_functions:
            
            if not cov_func_name in coverages:
                continue            
            
            cov = cov_func()
            
            if self.debug:
                print 'coverage %s: ' % (cov_func_name)
                print '             %f' % (cov)

            yield self.model.total_effort(), cov, cov_func_name

        if self.model.total_effort() < max_effort:
            for effort, coverage_frac, coverage_type in self.start_next_node(coverages, max_effort, next_func):
                yield effort, coverage_frac, coverage_type
        else:
            # finish signal!
            yield -1, None, None


    def start_supernode_degree(self, coverages=[0.20], max_effort=999999999):
        '''
        Supernode active strategies only work with lookahead > 0.
        '''
        self.model.strategy = 'start_supernode_degree'
        for effort, coverage_frac, coverage_type in self.start_supernode_order(coverages, max_effort, self.model.sorted_degrees_dec_iter(), 'start_supernode_degree'):
            yield effort, coverage_frac, coverage_type


    def start_supernode_random(self, coverages=[0.20], max_effort=999999999):
        '''
        Supernode active strategies only work with lookahead > 0.
        '''
        self.model.strategy = 'start_supernode_random'
        for effort, coverage_frac, coverage_type in self.start_supernode_order(coverages, max_effort, self.model.random_node_order_iter(), 'start_supernode_random'):
            yield effort, coverage_frac, coverage_type


    def start_supernode_order(self, coverages=[0.20], max_effort=None, nlist=[], name=None):
        '''
        Active attacks, a rogue node is added, and then nodes in nlist are linked to the supernode.
        Supernode active strategies only work with lookahead > 0.
        '''
        
        if len(coverages) < 1:
            raise PrivacyAttackStrategiesException('Error: strategies need a non-empty listo of graph float coverages!')

        rogue_node = str(random.random())[2:]
        self.model.add_agent_node( rogue_node )

        for node in nlist:

            if self.debug:
                print 'adding link from super node to node... %s -> %s' % (str(name),node)
                print 'lookahead %d' % self.model.lookahead

            if not self.model.graph.has_edge(rogue_node, node):    
                self.model.add_false_link(rogue_node, node)
            else:
                continue

            if self.debug:
                print 'effort: %d' % self.model.total_effort()
            
            for cov_func, cov_func_name in self.coverage_functions:

                if not cov_func_name in coverages:
                    continue
                
                cov = cov_func()
                
                if self.debug:
                    print 'coverage %s: ' % (cov_func_name)
                    print '             %f' % (cov)
    
                if cov >= coverages[cov_func_name][0]:                
                    while cov >= coverages[cov_func_name][0]:
                        yield self.model.total_effort(), coverages[cov_func_name][0], cov_func_name
                        coverages[cov_func_name] = coverages[cov_func_name][1:]
                        if len(coverages[cov_func_name]) == 0:
                            del coverages[cov_func_name]
                            break

            if self.model.total_effort() >= max_effort or len(coverages)==0:
                break

        # finish signal!
        yield -1, None, None
        

    def start_supernode_greedy(self, coverages=[0.20], max_effort=999999999):
        '''
        Supernode active strategies only work with lookahead > 0.
        '''
        self.model.strategy = 'start_supernode_greedy'
        return self.start_next_supernode(coverages, max_effort, self.model.max_unseen_degree_node)


    def start_supernode_crawler(self, coverages=[0.20], max_effort=999999999):
        '''
        Supernode active strategies only work with lookahead > 0.
        '''
        self.model.strategy = 'start_supernode_crawler'
        node = None
        for n in self.model.random_node_order_iter():
            node = n
            break
        # choose random node to start crawling...
        #node = self.model.random_node()

        for effort, coverage_frac, coverage_type in self.start_next_supernode(coverages, max_effort, self.model.max_unseen_degree_crawler_node, node):
            yield effort, coverage_frac, coverage_type


    def start_next_supernode(self, coverages=[0.20], max_effort=None, next_func=None, first_node=None):        
        '''
        Supernode active strategies only work with lookahead > 0.
        '''

        if len(coverages) < 1:
            raise PrivacyAttackStrategiesException('Error: strategies need a non-empty listo of graph float coverages!')

        rogue_node = str(random.random())[2:]
        self.model.add_agent_node( rogue_node )

        if first_node:

            node = first_node
            
            if self.debug:
                print 'adding link from super node to node... %s -> %s' % ('start_crawler()',node)
                print 'lookahead %d' % self.model.lookahead
            
            if not self.model.graph.has_edge(rogue_node, node):    
                self.model.add_false_link(rogue_node, node)

        if self.debug:
            print 'effort: %d' % self.model.total_effort()
        
            for cov_func, cov_func_name in self.coverage_functions:
                
                if not cov_func_name in coverages:
                    continue

                cov = cov_func()
                
                if self.debug:
                    print 'coverage %s: ' % (cov_func_name)
                    print '             %f' % (cov)
    
                if cov >= coverages[cov_func_name][0]:                
                    while cov >= coverages[cov_func_name][0]:
                        yield self.model.total_effort(), coverages[cov_func_name][0], cov_func_name
                        coverages[cov_func_name] = coverages[cov_func_name][1:]
                        if len(coverages[cov_func_name]) == 0:
                            del coverages[cov_func_name]
                            break

            if self.model.total_effort() >= max_effort or len(coverages)==0:
                # finish signal!
                yield -1, None, None
                return

        nc = 0
        while nc < self.model.graph.number_of_nodes():
            
            node = next_func()
            
            if self.debug:
                print 'adding link from super node to node... %s -> %s' % (str(next_func),node)
                print 'lookahead %d' % self.model.lookahead
                            
            if not self.model.graph.has_edge(rogue_node, node):    
                self.model.add_false_link(rogue_node, node)
            else:
                continue
            
            if self.debug:
                print 'effort: %d' % self.model.total_effort()
            
            for cov_func, cov_func_name in self.coverage_functions:
                
                if not cov_func_name in coverages:
                    continue

                cov = cov_func()
                
                if self.debug:
                    print 'coverage %s: ' % (cov_func_name)
                    print '             %f' % (cov)
    
                if cov >= coverages[cov_func_name][0]:                
                    while cov >= coverages[cov_func_name][0]:
                        yield self.model.total_effort(), coverages[cov_func_name][0], cov_func_name
                        coverages[cov_func_name] = coverages[cov_func_name][1:]
                        if len(coverages[cov_func_name]) == 0:
                            del coverages[cov_func_name]
                            break

            if self.model.total_effort() >= max_effort or len(coverages)==0:
                break
            
            nc += 1

        # finish signal!
        yield -1, None, None
            

    def start_generic(self, coverages=[0.20], max_effort=999999999, action_generator=None):

        if len(coverages) < 1:
            raise PrivacyAttackStrategiesException('Error: strategies need a non-empty list of graph float coverages!')

        nc = 0
        while nc < self.model.graph.number_of_nodes():

            action = action_generator()
            
            if self.debug:
                print 'executing action %s... ' % (str(action))
                print 'lookahead %d' % self.model.lookahead
                                
            action()

            if self.debug:
                print 'effort: %d' % self.model.total_effort()
            
            for cov_func, cov_func_name in self.coverage_functions:
                
                if not cov_func_name in coverages:
                    continue

                cov = cov_func()
                
                if self.debug:
                    print 'coverage %s: ' % (cov_func_name)
                    print '             %f' % (cov)
    
                if cov >= coverages[cov_func_name][0]:                
                    while cov >= coverages[cov_func_name][0]:
                        yield self.model.total_effort(), coverages[cov_func_name][0], cov_func_name
                        coverages[cov_func_name] = coverages[cov_func_name][1:]
                        if len(coverages[cov_func_name]) == 0:
                            del coverages[cov_func_name]
                            break

            if self.model.total_effort() >= max_effort or len(coverages)==0:
                break
            
            nc += 1
            
        # finish signal!
        yield -1, None, None

        
        
        
        
