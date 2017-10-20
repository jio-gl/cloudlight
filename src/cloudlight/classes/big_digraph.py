'''
Created on Apr 28, 2010

@author: jose
'''

from cloudlight.classes.big_graph import BigGraph
from cloudlight.classes.digraph import DiGraph


import sqlite3 as sql

import random, os


class BigDiGraphException(Exception):
    pass


class BigDiGraph(BigGraph):
    '''
    classdocs
    '''

    __basepath = '/tmp/'
    __cache_size_pages = 2**16


    def __db_filename(self):
        return self.__basepath + ('%s' % str(random.random()) + '.ldb')


    def __init__(self, name=None, cache_size=None):
        '''
        Choose a name to stored the database in /tmp/{name}. Otherwise a random name is chosen 
        and the db is not persistent.
        Is recommended to create the indices after the graph is loaded with method create_indices()
        '''

        super(BigDiGraph, self).__init__(name, cache_size)
                

    def add_edge(self, src, dst, weight=1):
        
        self.add_node(src)
        src_id = self.node_id(src)
        
        self.add_node(dst)
        dst_id = self.node_id(dst)
        
        c = self.conn.cursor()
        try:        
            # Insert a boths links
            c.execute("""insert into edges
              values (?, ?, ?)""", (src_id, dst_id, weight))
        except sql.IntegrityError:
            pass
        

    def number_of_edges(self):
        query = '''
        select count(*)
        from edges
        '''
        ret = None            
        for row in self.conn.cursor().execute(query):
            ret = row[0]
        return ret
    
                
    def edges(self):
        raise BigDiGraphException('Error: edges() not implemented, use edges_iter() !!!')

            
    def edges_iter(self, nbunch=None):
        
        if not nbunch:
            query = '''
            select distinct nodes1.node, nodes2.node 
            from nodes as nodes1, nodes as nodes2
            join edges
            where nodes1.id = edges.src and nodes2.id = edges.dst 
            '''            
            for row in self.conn.cursor().execute(query):
                    yield row[0], row[1]       
    
        else:
            
            query = '''
            select nodes1.node, nodes2.node 
            from nodes as nodes1, nodes as nodes2
            join edges
            where nodes1.id = edges.src and nodes2.id = edges.dst and nodes1.node = ?                
            '''
            
            if isinstance(nbunch, int) or isinstance(nbunch, str):
                nbunch = [nbunch]
                
            for node in nbunch:
                for row in self.conn.cursor().execute(query, (str(node),)):
                    yield row[0], row[1]    

            
    def degrees(self, nodes=None):
        raise BigDiGraphException('Error: degrees() not implemented in BigDiGraph, use BigGraph instead !!!')        

    
    def degrees_iter(self, nodes=None):
        raise BigDiGraphException('Error: degrees() not implemented in BigDiGraph, use BigGraph instead !!!')        


    def degree(self, node):
        raise BigDiGraphException('Error: degrees() not implemented in BigDiGraph, use BigGraph instead !!!')        

            
    def clustering_indices_iter(self, nodes=None):        
        raise BigDiGraphException('Error: degrees() not implemented in BigDiGraph, use BigGraph instead !!!')        

    
    def clustering_indices(self, nodes=None):        
        raise BigDiGraphException('Error: degrees() not implemented in BigDiGraph, use BigGraph instead !!!')        

            
    def neighbors(self, node):
        
        neighs = []
        for _, neigh in self.edges_iter([node]):
            neighs.append (  neigh )
        return neighs

    
    def add_only_symmetric_edgelist(self, graph):
        
        DiGraph.add_only_symmetric_edgelist_classmethod(self, graph)
        
    
