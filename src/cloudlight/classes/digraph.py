'''
Created on Mar 16, 2010

@author: jose
'''

from cloudlight.utils.misc import Base

import networkx as nx

import sys

class DiGraph(nx.DiGraph):
    '''
    A graph that extends NetworkX DiGraph with more analytic parameters and other things.
    '''

    debug = False
    input_debug_links = 100000
    output_debug_nodes = 10
    
    max_links_input = 10 ** 8
    max_nodes_analysis = 1000     


    def __init__(self):
        '''
        Constructor
        '''
        super(DiGraph, self).__init__()
        
        
    def load_edgelist(self, fileobj, num=False, use_big_alphabet=False):
        c = 0
        
        if use_big_alphabet:
            base = Base()
        
        for line in fileobj:
            if line.strip() == '' or line.strip()[0]=='#':
                continue
            s = line.split()
            if num:

                if use_big_alphabet:
                    src = base.base2num(s[0])
                    dst = base.base2num(s[1].strip())
                else:
                    src = int(s[0])
                    dst = int(s[1].strip())
                    
            else:
                src = s[0]
                dst = s[1].strip()
                
            self.add_edge(src, dst)
            c += 1
            if self.debug and c % self.input_debug_links == 0:
                sys.stdout.write('INFO: INPUT load_edgelist(), link count = %d\n' % c)
            if c >= self.max_links_input:
                break

        if self.debug:
            sys.stdout.write('INFO: FINISH INPUT load_edgelist(), link count = %d\n' % c)

    
    def add_only_symmetric_edgelist(self, graph):
        
        DiGraph.add_only_symmetric_edgelist_classmethod(self, graph)
        
    
    @classmethod    
    def add_only_symmetric_edgelist_classmethod(cls, digraph, graph):
        '''
        Save the symmetric subgraph into a undirected graph
        graph : undirected graph where the symmetric edges are added.
        '''

        for v, w in digraph.edges_iter():            
           
            if v < w and digraph.has_edge(w, v):
                
                graph.add_edge(v, w)