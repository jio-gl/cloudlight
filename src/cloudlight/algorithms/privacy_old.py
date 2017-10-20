'''
Created on Mar 19, 2010

@author: jose
'''

import random, copy

from cloudlight.classes.graph import Graph


class LinkPrivacyModelException(Exception):
    '''
    classdocs
    '''
    pass




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
        self.lookahead = lookahead + 1

        if self.debug:
            print 'INFO: Initializing LinkPrivacyModel...'
        
        self.rogues = set([]) # remember extra rogues nodes added
        self.false_links_graph = Graph() # remember false links added
        self.visible_graph = Graph() # infiltrated subgraph
        self.unseen_graph = copy.deepcopy(graph) # uninfiltrated subgraph

        self.rogue_effort = 0 # cost in new nodes created        
        self.bribe_effort = 0 # cost in existing nodes bribed        
        self.false_link_effort = 0 # cost in new links created
        
        self.cache_korolova_coverage = set([])
        self.cached_sorted_degrees_dec = None
        
    
    def add_rogue_node(self, r_node):

        if self.debug:
            print 'INFO: add_rogue_node --> %s ...' % str(r_node) 
        
        if r_node in self.graph.nodes():
            raise LinkPrivacyModelException('new rogue node "%s" already in friend graph!' % str(r_node))
        
        if r_node in self.rogues:
            raise LinkPrivacyModelException('new node "%s" already in rogue node set!' % str(r_node))
        
        self.rogues.add(r_node)    
        self.graph.add_node(r_node)
        self.visible_graph.add_node(r_node)

        self.rogue_effort += 1


    def add_bribed_node(self, r_node):

        if self.debug:
            print 'INFO: add_bribed_node --> %s ...' % str(r_node) 
        
        if not r_node in self.graph.nodes():
            raise LinkPrivacyModelException('new bribed node "%s" NOT in friend graph!' % str(r_node))

        self.visible_graph.add_node(r_node)
        
        edges = self.graph.lookahead_edges([r_node], self.lookahead)
        self.visible_graph.add_edges_from(edges)
        self.unseen_graph.remove_edges_from(edges)
        nodes_in_new_visible_edges = list(set([n for n,_ in edges] + [n2 for _,n2 in edges]))
        for node in nodes_in_new_visible_edges:  
#            if self.unseen_graph.has_node(node) and self.unseen_graph.degree(node) == 0:
#                self.unseen_graph.remove_node(node)
            if self.visible_graph.degree(node) == self.graph.degree(node):
                self.cache_korolova_coverage.add( node )

        self.bribe_effort += 1
#        self.cache_korolova_coverage.add( r_node )
#        for neigh in self.graph.neighbors(r_node):
#            if self.visible_graph.degree(neigh) == self.graph.degree(neigh):
#                self.cache_korolova_coverage.add( neigh )


    def add_false_link(self, src, dst):
        
        if not src in self.graph.nodes():
            raise LinkPrivacyModelException('new false link source node "%s" NOT in rogues or friend graph!' % str(src))
        if not dst in self.graph.nodes():
            raise LinkPrivacyModelException('new false link destination node "%s" NOT in rogues or friend graph!' % str(dst))

        self.false_links_graph.add_edge(src, dst)
        self.graph.add_edge(src, dst)

        if self.visible_graph.has_node(src): 
            self.visible_graph.add_edges_from(self.graph.lookahead_edges([src], self.lookahead))

        if self.visible_graph.has_node(dst): 
            self.visible_graph.add_edges_from(self.graph.lookahead_edges([dst], self.lookahead))

        self.false_link_effort += 1


    def link_coverage(self):
        numerator = float(self.visible_graph.number_of_edges() - self.false_links_graph.number_of_edges())
        denominator = float(self.graph.number_of_edges() - self.false_links_graph.number_of_edges())
        return numerator / denominator


    def node_coverage(self):
        numerator = float(self.visible_graph.number_of_nodes() - len(self.rogues))
        denominator = float(self.graph.number_of_nodes() - len(self.rogues))
        return numerator / denominator


    def korolova_node_coverage(self):
        #numerator = 0
        #for node in self.visible_graph.nodes_iter():
        #    if self.graph.degree(node) == self.visible_graph.degree(node):
        #        numerator += 1
                
        numerator = len( self.cache_korolova_coverage ) 
        denominator = float(self.graph.number_of_nodes() - len(self.rogues))
        return numerator / denominator


    def total_effort(self):
        return self.rogue_effort + self.bribe_effort + self.false_link_effort
        

    def max_unseen_degree_node(self):

        unseen_nodes_degrees = zip(self.unseen_graph.nodes(), self.unseen_graph.degrees())
        # in reverse order
        unseen_nodes_degrees.sort( lambda x, y: -cmp(x[1],y[1]) )
        
        return unseen_nodes_degrees[0][0]
    

    def max_unseen_degree_crawler_node(self):

        if self.debug:
            print 'INFO: max_unseen_degree_crawler_node ...' 

        unseen_nodes_degrees = zip(self.unseen_graph.nodes(), self.unseen_graph.degrees())
        # in reverse order
        unseen_nodes_degrees.sort( lambda x, y: -cmp(x[1],y[1]) )

        visible_node_with_max_unseen_degree = None
        for node, _ in unseen_nodes_degrees:
            if node in self.visible_graph.nodes():
                visible_node_with_max_unseen_degree = node
                break
        return visible_node_with_max_unseen_degree


    def sorted_degrees_dec(self):

        if self.debug:
            print 'INFO: sorted_degrees_dec ...' 

        if not self.cached_sorted_degrees_dec:

            degrees = zip(self.graph.nodes(), self.graph.degree())
            
            degrees.sort( lambda x, y : cmp(x[1], y[1]) )
            degrees.reverse()    
            
            self.cached_sorted_degrees_dec = [x for x, _ in degrees]
    
        return self.cached_sorted_degrees_dec
        

    def sorted_degrees_dec_iter(self):

        return iter(self.sorted_degrees_dec())
    
    
    def random_node_order(self):
        
        if self.debug:
            print 'INFO: random_node_order ...' 

        return self.graph.random_nodes(self.graph.number_of_nodes())


    def random_node_order_iter(self):

        return iter(self.random_node_order())
    
    
    def random_node(self):
        return self.graph.random_nodes(1)[0]



