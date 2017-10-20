#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on May 10, 2010

@author: jose
'''

import random
import time
import math


class LinkPrivacyModelException(Exception):
    '''
    classdocs
    '''
    pass


class SetMem:
    
    
    def __init__(self, list=[]):

        self.__rep = set(list)
        
        
    def add(self, elem):
        
        try:
            elem = int(elem)
        except:
            pass
            
        self.__rep.add(elem)


    def __contains__(self, elem):

        try:
            elem = int(elem)
        except:
            pass
            
        return elem in self.__rep

        
        

class LinkPrivacyModel(object):
    '''
    A class to simulate link privacy attacks on network with limited node visibility.
    '''


    def __init__(self, graph, lookahead, debug=False):
        '''
        graph:     graph where the attack is made.
        lookahead: visibility of the nodes in the graph.
        '''
        self.debug = debug
        self.graph = graph
        self.number_of_nodes = graph.number_of_nodes()
        self.number_of_edges = graph.number_of_edges()
        self.lookahead = lookahead

        if self.debug:
            print 'INFO: Initializing LinkPrivacyModel...'
        
        self.visible_edges_count = 0
        self.controlled_nodes = set([]) # remember extra rogues nodes added
        self.agents = set([])
        self.false_links = [] # remember false links added

        self.agents_effort = 0 # cost in new nodes created        
        self.bribe_effort = 0 # cost in existing nodes bribed        
        self.false_link_effort = 0 # cost in new links created
        
        self.__unseen_param_key = 'unseen_degree'
        self.__unseen_triangles_param_key = 'unseen_triangles'
        self.__seen_triangles_param_key = 'seen_triangles'
        self.__seen_triangles2_param_key = 'seen_triangles2'
        self.__seen_param_key = 'seen_degree'
        self.__seen2_param_key = 'seen_degree2'
        
        self.strategy = None
        self.coverage_type = None

        self.__total_triangles = self.graph.total_triangles()
        
        #self.__init_unseen_degree()
        #self.graph.remove_index_parameter_cache(self.__unseen_param_key)
        #self.graph.reset_edge_weights()


    def __init_unseen_degree(self):
       
        self.graph.remove_index_parameter_cache(self.__unseen_param_key)
        self.graph.remove_parameter_cache(self.__unseen_param_key)
        
        self.graph.add_parameter_cache(self.__unseen_param_key)
        
        total_nodes = self.graph.number_of_nodes()
        
        count = 0
        if self.debug:
            print 'INFO: __init_unseen_degree %d nodes of %d nodes total ...' % (count, total_nodes) 

        for node, degree in self.graph.get_parameter_cache_iter('degree'):
            
            self.graph.insert_parameter_cache(self.__unseen_param_key, node, degree)
            count += 1
            if self.debug and count % 100000 == 0:
                print 'INFO: __init_unseen_degree %d nodes of %d nodes total ... %s' % (count, total_nodes, time.ctime()) 

        print 'INFO: __init_unseen_degree %d nodes of %d nodes total ...' % (count, total_nodes) 

        self.graph.index_parameter_cache( self.__unseen_param_key )
        
    
    def add_agent_node(self, r_node):

        if self.debug:
            print 'INFO: add_rogue_node --> %s ...' % str(r_node) 
        
        if self.graph.has_node( r_node ):
            raise LinkPrivacyModelException('new rogue node "%s" already in friend graph!' % str(r_node))
        
        if r_node in self.controlled_nodes:
            raise LinkPrivacyModelException('new node "%s" already in rogue node set!' % str(r_node))
        
        self.controlled_nodes.add(r_node)
        self.agents.add( r_node )    
        self.graph.add_node(r_node)
        
#        if self.using_unseen_degree():  
#            self.graph.insert_parameter_cache(self.__unseen_param_key, r_node, 0)
#        
#        if self.using_unseen_triangles() and self.lookahead > 0:  
#            self.graph.insert_parameter_cache(self.__unseen_triangles_param_key, r_node, 0)
#        
#        if self.using_seen_triangles() and self.lookahead > 0:  
#            new_triangles_node = self.graph.get_parameter_cache('triangles', r_node)
#            self.graph.insert_parameter_cache(self.__seen_triangles_param_key, r_node, new_triangles_node)
        
        self.__visited = SetMem()
        self.__add_bribed_node_recursive(r_node, self.lookahead)
        
        self.agents_effort += 1


    def using_unseen_degree(self):
        return (self.strategy and ('start_greedy' == self.strategy or 'start_crawler' == self.strategy or 'start_crawler_triangles' == self.strategy or 'start_crawler_seen_triangles' == self.strategy)) or ('korolova' in self.coverage_types or 'complete_node' in self.coverage_types)  
                

    def using_unseen_triangles(self):
        return (self.strategy and ('greedy_triangles' in self.strategy or 'crawler_triangles' in self.strategy))
                

    def using_seen_triangles(self):
        return ('triangle' in self.coverage_types) or (self.strategy and ('greedy_seen_triangles' in self.strategy or 'crawler_seen_triangles' in self.strategy  or 'crawler_degree_hist_bin_dist_orderby_triangles' in self.strategy))
                

    def using_seen_degree(self):        
        return self.using_degree_hist() or ('node' in self.coverage_types) or (self.strategy and ('greedy_seen_degree' in self.strategy or 'crawler_seen_degree' in self.strategy or 'crawler_random' in self.strategy))
                

    def add_bribed_node(self, r_node):

        if self.debug:
            print 'INFO: add_bribed_node --> %s ...' % str(r_node) 
        
        #if not self.graph.has_node( r_node ):
        #    raise LinkPrivacyModelException('new bribed node "%s" NOT in friend graph!' % str(r_node))

        self.__visited = SetMem()
        self.__add_bribed_node_recursive(r_node, self.lookahead)
        
        self.controlled_nodes.add(r_node)    

        self.bribe_effort += 1


    def __add_bribed_node_recursive(self, r_node, lookahead):
        '''
        Pseudo-codigo sobornar_nodo_recursiva( nodo, lookahead):
            Notas:
                - visitados se inicializa antes de la primara llamada en Vacio
                - aristas_visibles es persistente y ya viene con valores marcados de otros nodos sobornados de forma no-recursiva.
                        
        grado_no_visto[nodo] :=  0
        histograma_grado[ grado_visto2[nodo] ] -= 1
        histograma_grado[ grado[nodo] ] += 1
        grado_visto1[nodo] := -1
        grado_visto2[nodo] := grado[nodo]
        
        visitados.agregar( nodo )
        
        para cada arista (nodo -- vecino) hacer:

            si no pertenece (nodo -- vecino) a aristas_visibles hacer:
            
                aristas_visibles.agregar( (nodo -- vecino) ] )

                si grado_visto1[vecino] no es -1 hacer:
                    histograma_grado[ grado_visto1[vecino] ] -= 1
                    histograma_grado[ grado_visto1[vecino] + 1 ] += 1
                    grado_visto1[vecino] := grado_visto1[vecino] + 1
                    grado_visto2[vecino] := grado_visto2[vecino] + 1
                    grado_no_visto[vecino] := grado_no_visto[vecino] - 1
            
        si triangulos_vistos2[nodo] no es -1 entonces:
            si lookahead > 0 entonces:
                triangulos_no_vistos[nodo] := 0 
                triangulos_vistos1[nodo] := triangulos[nodo]
                triangulos_vistos2[nodo] := -1 
            en cambio si lookahead = 0 entonces:
                triangulos_vistos1[nodo] := computar_triangulos_vistos(nodo) 
                triangulos_vistos2[nodo] := computar_triangulos_vistos(nodo)
                triangulos_no_vistos[nodo] := triangulos[nodo] - computar_triangulos_vistos(nodo)

        para cada arista (nodo -- vecino) hacer:

            si triangulos_vistos2[vecino] no es -1 hacer:
                triangulos_vistos1[vecino] := computar_triangulos_vistos(vecino) 
                triangulos_vistos2[vecino] := computar_triangulos_vistos(vecino)
                triangulos_no_vistos[vecino] := triangulos[vecino] - computar_triangulos_vistos(vecino)
            
            si no pertenece vecino a visitados y lookahead > 0 hacer:            
                sobornar_nodo_recursiva( vecino, lookahead - 1)
            
        '''
        

        # if unseen degree is 0, then node is fully visible...
        if self.using_unseen_degree():
            self.graph.update_parameter_cache(self.__unseen_param_key, r_node, 0)

        # seen degree -1 means all degree is visible
        if self.using_seen_degree() and self.graph.get_parameter_cache(self.__seen_param_key, r_node) != -1:
            self.graph.update_parameter_cache(self.__seen_param_key, r_node, -1)
            r_node_degree = self.graph.get_parameter_cache('degree', r_node)
            if self.using_degree_hist():
                self.update_degree_hist_fixed(r_node_degree)
            previous_r_node_degree = self.graph.get_parameter_cache(self.__seen2_param_key, r_node)
            #print 'POR ACTUALIZAR R_NODE DEG HIST: PREV DEG %d  DEG %d' % (previous_r_node_degree, r_node_degree)            
            if previous_r_node_degree != r_node_degree:
                self.graph.update_parameter_cache(self.__seen2_param_key, r_node, r_node_degree)
                if self.using_degree_hist():
                    #print 'ACTUALIZANDO R_NODE DEG HIST: NODO %s PREV %d NEW %d' % (r_node, previous_r_node_degree, r_node_degree)
                    self.update_degree_hist(r_node, previous_r_node_degree, r_node_degree)                    
            
        #print 'VISITANDO NODO --> %s   LOOKAHEAD %d' % (r_node, lookahead)
        self.__visited.add( r_node )
        
        for neigh in self.graph.neighbors_iter( r_node, upper_bound_weigh=1 ): # visible edges neighbors with weight <= 1
    
            self.graph.update_edge_weight( r_node, neigh, 2) # mark as visible, 2 == visible
            #print 'ARISTA VISITADA %s -- %s' % (r_node, neigh)
            
            self.visible_edges_count += 1

            if lookahead == 0 and self.graph.get_parameter_cache(self.__seen_param_key, neigh) != -1:
                if self.using_unseen_degree():
                    self.graph.dec_parameter_cache(self.__unseen_param_key, neigh) # decrease unseen degree
                    
                if self.using_seen_degree():
                    self.graph.inc_parameter_cache(self.__seen_param_key, neigh) # increase seen degree
                    previous_neigh_degree = self.graph.get_parameter_cache(self.__seen2_param_key, neigh)
                    self.graph.inc_parameter_cache(self.__seen2_param_key, neigh) # increase seen degree                
                    if self.using_degree_hist():
                            #print 'ACTUALIZANDO NEIGH DEG HIST: NODO %s PREV %d NEW %d' % (neigh, previous_neigh_degree, previous_neigh_degree+1)
                            self.update_degree_hist(neigh, previous_neigh_degree, previous_neigh_degree+1)

        if self.using_seen_triangles() or self.using_unseen_triangles():
            #print 'updating seen_triangles and unseen_triangles   ... node = ', r_node
            if self.graph.get_parameter_cache(self.__seen_triangles2_param_key, r_node) != -1:
                if lookahead > 0:
                    #print 'lookahead > 0'
                    self.graph.update_parameter_cache(self.__unseen_triangles_param_key, r_node, 0)
                    new_triangles_node = self.graph.get_parameter_cache('triangles', r_node)
                    self.graph.update_parameter_cache(self.__seen_triangles_param_key, r_node, new_triangles_node)
                    self.graph.update_parameter_cache(self.__seen_triangles2_param_key, r_node, -1)
                else:
                    
                    #print 'lookahead == 0'
                    seen_triangles_node = self.graph.triangles_weight(r_node, 2) # 2 == visible 
                    self.graph.update_parameter_cache(self.__seen_triangles_param_key, r_node, seen_triangles_node)
                    self.graph.update_parameter_cache(self.__seen_triangles2_param_key, r_node, seen_triangles_node)
                    unseen_triangles_node = self.graph.triangles([r_node])[0] -  seen_triangles_node # 1 == not visible yet                
                    self.graph.update_parameter_cache(self.__unseen_triangles_param_key, r_node, unseen_triangles_node)
                    #if unseen_triangles_node == 0:
                    #    self.graph.update_parameter_cache(self.__seen_triangles2_param_key, r_node, -1)

        for neigh in self.graph.neighbors_iter( r_node, upper_bound_weigh=2 ): # all neighbors

            if lookahead == 0 and (self.using_unseen_triangles() or self.using_seen_triangles()): # update unseen_triangles and seen triangles for neighbor
                
                if self.graph.get_parameter_cache(self.__seen_triangles2_param_key, neigh) != -1:
                
                    # update seen_triangles
                    seen_triangles_neigh = self.graph.triangles_weight(neigh, 2) # 2 == visible 
                    self.graph.update_parameter_cache(self.__seen_triangles_param_key, neigh, seen_triangles_neigh)
                    self.graph.update_parameter_cache(self.__seen_triangles2_param_key, neigh, seen_triangles_neigh)
                    # update unseen_triangles, complement of seen_triangles
                    unseen_triangles_neigh = self.graph.get_parameter_cache('triangles', neigh) -  seen_triangles_neigh # 1 == not visible yet
                    self.graph.update_parameter_cache(self.__unseen_triangles_param_key, neigh, unseen_triangles_neigh)
                
            if lookahead > 0 and not neigh in self.__visited:             
                    
                self.__add_bribed_node_recursive(neigh, lookahead - 1)




    def add_false_link(self, src, dst):
        '''
        Assuming nothing, should work if src or dst are controlled by the attacker or 
        any controlled node is in the range of the new link!            
        '''

        #if not src in self.controlled_nodes and not dst in self.controlled_nodes :
        #    raise LinkPrivacyModelException('Error: nor node %s nor %s are controlled nodes!' % (src,dst))

        self.false_links.append( (src, dst) )
        
        # assuming edge not exists
        self.graph.add_edge( src, dst )
        self.graph.update_edge_weight( src, dst, 2) # mark as visible, 2 == visible
        self.visible_edges_count += 1

        # found controlled node at minimum distance
        self.__visited = SetMem()
        controlled_node_min_distance, _  = self.__found_controlled_recursive(src, src, self.lookahead, self.lookahead)
        if controlled_node_min_distance:
            self.__visited = SetMem()
            self.__add_bribed_node_recursive(controlled_node_min_distance, self.lookahead)

        self.false_link_effort += 1


    def __found_controlled_recursive(self, center, r_node, lookahead, initial_lookahead):
        '''
        Found closer node in neighborhood of center that is controlled.
        '''
        
        if r_node in self.controlled_nodes:
            return r_node, initial_lookahead - lookahead
            
        #self.graph.update_parameter_cache('visited', r_node, 1.0)
        self.__visited.add( r_node )

        candidate, candidate_distance = None, 9999999
        #print list(self.graph.neighbors_iter( r_node ))
        for neigh in self.graph.neighbors_iter( r_node ):
    
            if lookahead > 0 and not neigh in self.__visited:             
                
                ret, ret_dist = self.__found_controlled_recursive(center, neigh, lookahead - 1, initial_lookahead)
                
                if ret and ret_dist < candidate_distance:
                    candidate = ret
                    candidate_distance = ret_dist
    
        return candidate, candidate_distance


    def link_coverage(self):
        
        
        numerator = float(self.visible_edges_count - self.false_link_effort)
        denominator = float(self.graph.number_of_edges() - self.false_link_effort)
        return numerator / denominator


    def node_coverage(self):
        
        #raise LinkPrivacyModelException('Unimplemmented: method node_coverage() untested!')

        # seen nodes have seen degree greater than 0 
        numerator1 = self.graph.get_parameter_cache_inverse_count_gt(self.__seen2_param_key, 0)
        numerator2 = 0
        #numerator2 = self.graph.get_parameter_cache_inverse_count_lt(self.__seen_param_key, 0)
        denominator = self.number_of_nodes
        
        return (float(numerator1 + numerator2) / denominator)


    def korolova_node_coverage(self):
        numerator = self.graph.get_parameter_cache_inverse_count(self.__unseen_param_key, 0)
        denominator = self.number_of_nodes
        return float(numerator) / denominator


    def triangle_coverage(self):
        
        #numerator = float(self.__total_triangles - self.graph.total_unseen_triangles())        
        numerator = float(self.graph.total_seen_triangles())
        denominator = float(self.__total_triangles)
        
        #print 'numerator', numerator
        #print 'denominator', denominator
        if denominator == 0.0:
            return 1.0
        return ( numerator / denominator )


    def total_effort(self):
        return self.agents_effort + self.bribe_effort + self.false_link_effort
        

    def max_unseen_degree_node(self):

        node = None
        for max_node, _ in self.graph.get_parameter_cache_iter(self.__unseen_param_key):
            node = max_node
            break
        return node 
    

    def max_unseen_degree_crawler_node(self):

        node = None
        #print 'START max_unseen_degree_crawler_node: unseen_degree_Table: '
        for next_node, unseen_degree_val in self.graph.get_parameter_cache_iter(self.__unseen_param_key):
            
            degree_next_node = self.graph.get_parameter_cache('degree', next_node)
            
            # check if node seen by attack, that is the unseen degree is not complete
            if 0 < unseen_degree_val != degree_next_node:
                #print self.graph.get_parameter_cache(self.__unseen_param_key, next_node), self.graph.get_parameter_cache('degree', next_node) 
                node = next_node
                break
            
#        if node == None:
#            for next_node, seen_triangles in self.graph.get_parameter_cache_iter(self.__seen_triangles_param_key):
#                print next_node, seen_triangles
                
            
        return node 


    def max_unseen_triangles_node(self):

        node = None
        for max_node, _ in self.graph.get_parameter_cache_iter(self.__unseen_triangles_param_key):
            node = max_node
            break

        return node 


    def max_seen_degree_node(self):

        #for max_node, seen_degree in self.graph.get_parameter_cache_iter(self.__seen_param_key):
        #    print max_node, seen_degree
        
        node = None
        for max_node, _ in self.graph.get_parameter_cache_iter(self.__seen_param_key):
            node = max_node
            break
        return node 
    

    def max_seen_triangles_node(self):

        node = None
        for max_node, _ in self.graph.get_parameter_cache_iter(self.__seen_triangles2_param_key):
            node = max_node
            break
        return node 
    

    def max_unseen_triangles_crawler_node(self):

        if self.debug:
            print 'INFO: max_unseen_triangles_crawler_node ...' 

        node = None
        # ordered by unseen triangles, decrementaly
        for next_node, _ in self.graph.get_parameter_cache_iter(self.__unseen_triangles_param_key):

            # check if node seen by attack, that is the unseen degree is not complete
            #print next_node, 
            if self.graph.get_parameter_cache(self.__unseen_param_key, next_node) != self.graph.get_parameter_cache('degree', next_node):
                node = next_node
                break
            
        return node 


    def max_seen_degree_crawler_node(self):
        '''
        Only works with connected graphs!!!
        '''
        
        if self.debug:
            print 'INFO: max_seen_degree_crawler_node ...' 

        node = None
        # ordered by seen degrees, decrementaly
        for next_node, seen_degree in self.graph.get_parameter_cache_iter(self.__seen_param_key):
            
            # check if node seen by attack, that is the unseen degree is not complete
            #print next_node, seen_degree, self.graph.get_parameter_cache('degree', next_node)    
            if seen_degree > 0: # inside the visible graph
                node = next_node
                 
                break
            
        return node 


    def max_seen_triangles_crawler_node(self):
        '''
        Only works with connected graphs!!!
        '''
        
        if self.debug:
            print 'INFO: max_seen_triangles_crawler_node ...' 

        node = None
        # ordered by unseen triangles, decrementaly
        for next_node, _ in self.graph.get_parameter_cache_iter(self.__seen_triangles2_param_key):
            
            # check if node seen by attack, that is the unseen degree is not complete
            #print next_node, seen_triangles, self.graph.get_parameter_cache('degree', next_node)    
            if self.graph.get_parameter_cache(self.__unseen_param_key, next_node) != self.graph.get_parameter_cache('degree', next_node):
                node = next_node
                 
                break
            
        return node 


    def random_crawler_node(self):
        '''
        Only works with connected graphs!!!
        '''
        
        if self.debug:
            print 'INFO: random_crawler_node ...' 

        node = None
        for next_node in self.graph.get_parameter_cache_inverse_gt(self.__seen_param_key, 0, random=True):
#        for next_node, _ in self.graph.get_parameter_cache_inverse_count_gt(self.__seen_param_key, 0):
            node = next_node
            break
            
        return node 


    def sorted_degrees_dec_iter(self):

        if self.debug:
            print 'INFO: sorted_degrees_dec ...' 

        for node, _ in self.graph.get_parameter_cache_iter('degree'):
            yield node
        

    def sorted_triangles_dec_iter(self):

        if self.debug:
            print 'INFO: sorted_triangles_dec ...' 

        for node, _ in self.graph.get_parameter_cache_iter('triangles'):
            yield node
        

    def sorted_degrees_dec(self):

        raise LinkPrivacyModelException('NotImplemented: use sorted_degrees_dec_iter() instead!!!')


    def random_node_order_iter(self):
        
        if self.debug:
            print 'INFO: random_node_order ...' 

        use_random = True
        for node, _ in self.graph.get_parameter_cache_iter('degree', random=use_random):
            yield node


    def random_node_order(self):
        
        raise LinkPrivacyModelException('NotImplemented: use random_node_order_iter() instead!!!')


    def random_node(self):
        
        node = None
        for next_node in self.random_node_order_iter():
            node = next_node
            break
            
        return node


    def __del__(self):
        
        for agent_node in self.agents:
            
            self.graph.remove_node( agent_node )
            
        for src, dst in self.false_links:
            
            try:
                self.graph.remove_edge( src, dst )
            except:
                pass


    def initialize_histogram_degree( self):

        deg_dict = {}
        for _, deg in self.graph.get_parameter_cache_iter('degree'):
            deg = int(deg)
            if not deg in deg_dict:
                deg_dict[deg] = 0
            deg_dict[deg] += 1
            
        self.N = []
        for deg in range(max(deg_dict.keys())+1):
            
            if not deg in deg_dict.keys():
                
                self.N.append( 0 )
                
            else:
                
                self.N.append( deg_dict[deg] )
            
        self.__deg_hist_max = len(self.N) - 1
    
        # init accum degree table.
        self.M = [0]*len(self.N)
        self.n = [0]*len(self.N)
        self.M[0] = self.graph.number_of_nodes()
        self.Dmax = len(self.N) - 1


    def initialize_histogram_degree_dist( self, degree_dist=None, number_of_nodes=None, max_degree = 10000 ):
        '''
        Initialize degree histogram, assuming connected graph and power-law degree dist.
        
        
        '''
        histogram_total = number_of_nodes
        deg_hist = []
        deg = 1
        est_total = 0
        while True:
        #for deg in range(1, max_degree+1):
            
            est_nodes_per_deg = round( degree_dist( deg ) * histogram_total )
            
            if est_nodes_per_deg == 0:
                break
                #continue
            
            #if est_total >= histogram_total:
            #    deg_hist.append( 0 )                
            #else:
            deg_hist.append( est_nodes_per_deg )
            est_total += est_nodes_per_deg
            deg += 1
            
        deg_hist += [0]*len(deg_hist)

        deg_hist = [0] + deg_hist
        
        # correct deviation from number_of_nodes        
        factor = float(histogram_total) / float(est_total)        
        deg_hist = [ round(freq * factor) for freq in deg_hist ]            
        error = sum(deg_hist) - histogram_total        
        # correct error
        self.__deg_table_min = 1        
        self.__deg_hist_max = len(deg_hist) - 1

        self.N = deg_hist        
        self.N[self.__deg_table_min] += error
        
        
        print 'APROX DEGREE HISTOGRAM !!! len = %d  nodes = %d' % (len(self.N), self.graph.number_of_nodes()) 
        print self.N
        print 

        print 'REAL DEGREE HISTOGRAM !!! len = %d' % len(self.N)
        deg_dict = {}
        for _, deg in self.graph.get_parameter_cache_iter('degree'):
            deg = int(deg)
            if not deg in deg_dict:
                deg_dict[deg] = 0
            deg_dict[deg] += 1
            
        self.Nreal = []
        for deg in range(max(deg_dict.keys())+1):
            
            if not deg in deg_dict.keys():
                
                self.Nreal.append( 0 )
                
            else:
                
                self.Nreal.append( deg_dict[deg] )
            
        print self.Nreal
        print 


        
        
    
        # init accum degree table.
        self.M = [0]*len(deg_hist)
        self.n = [0]*len(deg_hist)
        self.Dmax = len(deg_hist) - 1
    
    
    def using_degree_hist(self):
        
        return self.strategy and ('start_crawler_degree_hist' in self.strategy or 'start_crawler_degree_aprox_hist_bin_dist' in self.strategy)
    

    def update_degree_hist(self, node, prev_deg, deg):
        
        #if prev_deg > 0: # para grado 0 no hay interes en contar nada.
        self.M[int(prev_deg)] -= 1
        
        #try:
        self.M[int(deg)] += 1
        #except:
        #    print 'ERROR deg = %f   M = %s' % (deg, str(self.M))
    
    
    def update_degree_hist_fixed(self, degree):
        '''
        Update histogram for nodes we know for sure that we have seen the complete degree.
        '''
        try:
            self.n[int(degree)] += 1
        except:
            print 'ERROR in histogram: degree = %d' % degree
            raise Exception('ERROR in histogram: degree = %d' % degree)
    
    
    def average_degree_jump_bin_distribution(self):

        # 1. Sea ei = 0 para i = 1, 2, ... , Dmax .
        e = [0.0] * len(self.N)
        # 2. Sea Bi = Ni − ni para i = 1, 2, ... , Dmax .
        B = [ N_i - n_i for N_i, n_i in zip(self.N, self.n) ]
        # a "m" también lo calculo ahora pq no lo tengo.        
        m = [ M_i - n_i for M_i, n_i in zip(self.M, self.n) ]
        
        # 3. Sea I = Dmax
        # 4. Mientras I > 0 hacemos lo siguiente:
        I = self.Dmax
        while I > 0: 
            
            # a) Sea J = max {i ≤ I : mi = 0}
            aux_list = [(i, m_i) for i, m_i in zip(range(0,I+1),m[:I+1]) if m_i != 0]
            #    Si mi = 0 para todo i ≤ I, se sale del algoritmo.
            if len(aux_list) == 0:
            
                break # si m_i para todo i <= I, se sale del algoritmo
            
            else:
                # maximo i con m_i != 0
                J = aux_list[-1][0] 
                
                # b) Definimos: CJ = \sum_{i=J}^[D_max] B_i
                C_J = sum(B[J:])

                # c) Para cada i ≥ J, definimos pi = B_i / C_J                
                p = [ C_J > 0.0 and B[i] / C_J or 0.0 for i in range(self.Dmax+1)]

                # d) Sea e_J = \sum_{i=J}^{Dmax} i*p_i − J.
                e[J] = sum( [ i*p[i] for i in range(J, self.Dmax+1)] )
                
                # e) Para cada i ≥ J, cambiamos
                #   Bi = Bi − pi · mJ .
                for i in range(J, self.Dmax+1):
                    B[i] = B[i] - p[i] * m[J]
                    
                # f ) Sea I = J − 1.
                I = J - 1
    
        return e


    def average_degree_jump_bin_distribution_random(self):

        # a "m" también lo calculo ahora pq no lo tengo.        
        self.m = [ M_i - n_i for M_i, n_i in zip(self.M, self.n) ]

        # 1. Sea A = {i ≤ Dmax : mi = 0}
        A = [i for i in range(self.Dmax+1) if self.m[i] != 0]

        # 2. Sea B_i = N_i − n_i para i = 1, 2, · · · , Dmax .
        B = [ N_i - n_i for N_i,n_i in zip(self.N, self.n) ]

        # 3. Para cada j ∈ A sea p^j_i,0 = B_i / \sum^Dmax_k=j B_k para i = j, j + 1, · · · , Dmax .
        p_prev = dict( [ ((j,i), B[i]/sum(B[j:self.Dmax+1])) for j in A for i in range(j,self.Dmax+1) ] ) 
        
        # 4. Sea n = 0.
        n = 0
        MAXITER = len(A) * 2
        eps_conv = 0.05
        random.seed(MAXITER)
        
        # 5. Hacemos lo siguiente:
        while True: # outer loop
            
            # a) Sea n = n + 1.
            n = n + 1
            
            while True: # inner loop
                # b) Elegimos J ∈ A.
                J = A[random.randint(0,len(A)-1)]

                # c) Para cada i ≥ J, cambiamos Bi = Bi − p^J_{i,n−1} * m_J 
                B = B[:J] + [ B_i - p_prev[(J,i)] * self.m[J] for B_i in B[J:] ]
                
                # d) Si Bi < 0 para algun i, reseteamos Bi = Ni − ni para i = 1, 2, · · · , Dmax y vamos nuevamente a b.
                if len([B_i for B_i in B if B_i < 0]) == 0:
                    break # inner loop
                else:
                    B = [ N_i - n_i for N_i,n_i in zip(self.N, self.n) ]

            # e) Para cada I ∈ A − {J}
            #     p^I_i,n = Bi / \sum^Dmax_i=I para i = I, I + 1, · · · , Dmax .
            p = dict( [ ((I,i), sum(B[I:self.Dmax+1])>0 and B[i]/sum(B[I:self.Dmax+1] or 0.0)) for I in A if I!=J for i in range(I,self.Dmax+1) ] )
            
            # f ) Definimos p^J_i,n = p^J_i,n−1 para i = J, J + 1, · · · , Dmax .
            for i in range(J,self.Dmax+1):
                p[(J,i)] = p_prev[(J,i)]
                
            # g) Volvemos a a) si n < MAXITER y || p^j_i,n − p^ji,n-1 || < eps_conv
            norm = sum( [abs( p[(j,i)] - p_prev[(j,i)] ) for j in A for i in range(j,self.Dmax+1) ] )
            if norm > eps_conv and n < MAXITER:
                p_prev = p
                continue # outer loop
            break

        # 6. Sea ei = 0 para i = 1, 2, · · · , Dmax .
        e = [0.0] * (self.Dmax+1)
        
        # 7. Para cada j ∈ A sea e_j = \sum_{i=j}^Dmax i * p^j_{i,n}  - j
        for j in A:
            e[j] = sum( [ i * p[(j,i)] for i in range(j,self.Dmax+1) ] ) - j
    
        return e


    def average_degree_jump(self):
        
        B = [ N_i - M_i for N_i, M_i in zip(self.N, self.M) ]

        e, j = [], 0        
        for j in range(self.Dmax+1):

            if j > 0:

                degs_right = range(j, self.Dmax+1)
                sum_B_j_slice = sum(B[j:])
                if sum_B_j_slice > 0:
                    e_j = sum( [ i * float(B_i) for i, B_i in zip(degs_right, B[j:])] )
                    e_j = (e_j / sum_B_j_slice) - j
                else:
                    e_j = 0.0
                e.append(e_j)
                
            else:
                
                e.append( 0.0 )
                
        return e


    def histogram_degree_crawler_node_bin_dist(self):
        return self.histogram_degree_crawler_node(bin_distribution=True, use_random_distribution=False )


    def aprox_histogram_degree_crawler_node_bin_dist(self):
        return self.histogram_degree_crawler_node(bin_distribution=True, use_random_distribution=False )


    def histogram_degree_crawler_node_bin_dist_orderby_triangles(self):
        return self.histogram_degree_crawler_node(bin_distribution=True, use_random_distribution=False, with_max_seen_triangles=True )


    def histogram_degree_crawler_node_bin_dist_rand(self):
        return self.histogram_degree_crawler_node(bin_distribution=True, use_random_distribution=True )


    def histogram_degree_crawler_node(self, bin_distribution=False, use_random_distribution=False, with_max_seen_triangles=False ):
        '''
        Get some node with high probability of having more unseen degree.
        
        - Si el grado de los nodos va de 0 a Dmax.
        - Para cada grado i, tiene ni nodos visitados y cubiertos completamente
        (es decir, sabe con certeza que su grado es i) y mi nodos con grado visto
         i de los que no sabe con certeza el grado real.
        - Llamemos M_i = n_i + m_i y B_i = N_i − M_i . Los B_i se definen de otra manera
          para las optimizaciones con distribucion de los m_i entre los bins.
        '''
        
        if not bin_distribution:

            e = self.average_degree_jump()
                
        else:
            
            if not use_random_distribution:
                
                e = self.average_degree_jump_bin_distribution()
                
            else:
                
                e = self.average_degree_jump_bin_distribution_random()
    
                
        jumps_tuples = zip( e, range(len(e)) )
        jumps_tuples.sort( lambda x,y : x[0] < y[0] and 1 or -1 )
        
        n = None
        for e_j, degree in jumps_tuples:

            n = self.choose_node_with_degree(degree, with_max_seen_triangles)            
            if n:
                break
          
        #if not n:
        #    raise Exception('not-fully visible node not found in histogram_degree_crawler_node()!')  
    
        return n


    def choose_node_with_degree(self, degree, with_max_seen_triangles):
        
        n = None
        
        if not with_max_seen_triangles:

            for node in self.graph.get_parameter_cache_inverse(self.__seen_param_key, degree):
                n = node
                break
            
        else: # use information about seen triangles

            for node in self.graph.get_parameter_cache_inverse_orderby(self.__seen_param_key, degree, self.__seen_triangles_param_key):
                n = node
                break
            
        return n

    
if __name__ == '__main__':
    
    model = LinkPrivacyModel()
