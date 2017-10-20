'''
Created on Apr 20, 2010

@author: jose
'''

from cloudlight.classes.graph import Graph
from cloudlight.utils.estimator import TimeEstimator
from itertools import izip

import sqlite3 as sql
import random, os, re, time


class BigGraphException(Exception):
    pass


class BigGraph(Graph):
    '''
    classdocs
    '''

    __cache_size_pages = 2**16


    def __db_filename(self):
        return self.__basepath + ('%s' % str(random.random()) + '.ldb')


    def __init__(self, name=None, cache_size=None):
        '''
        Choose a name to stored the dabatabse in /tmp/{name}. Otherwise a random name is chosen 
        and the db is not persistant.
        Is recommended to create the indieces after the graph is loaded with method create_indices()
        '''
        
        self.__basepath = '/tmp/'
        self.name = 'no_name'
        
        if cache_size:
            self.__cache_size_pages = cache_size

        if name:
            filename = name
            self.persistant = True
        else:
            filename = self.__db_filename() #
            self.persistant = False
             
        self.__filename = filename
        
        self.conn = sql.connect( self.__filename )
        c = self.conn.cursor()

        # Set cache size in pages
        c.execute('pragma cache_size = %d;' % self.__cache_size_pages)
        # little optimization
        c.execute('pragma count_change = off;')            
        c.execute('pragma temp_store = MEMORY;')
        c.execute('pragma synchronous=on;')            
        
        try:
            
            # Create table for nodes
            c.execute('''create table nodes
                        (node text, id integer primary key)''')
            
            # Create table for edges
            c.execute('''create table edges                        
                        (src integer, dst integer, weight integer)''')
                        #(src integer, dst integer)''')
            
            # Create index for nodes
            c.execute('''create index if not exists 
                    nodes_index on nodes (node)''')
        except sql.OperationalError: # only create tables the first time
            pass
        
        class Adj(object):
            self.__contains__ = self.__contains__
        self.adj = Adj()
                

    def create_indices(self):
        c = self.conn.cursor()
        
        # Create index for edges
        c.execute('''create unique index if not exists 
                    edges_index on edges (src, dst, weight)''')
#        c.execute('''create index if not exists 
#                    edges_index on edges (src, dst, weight)''')
        
        #self.create_index_degree()
        #self.create_index_clustering()
        #self.create_index_knn()


    def create_index_degree(self):

        self.index_parameter_generic('degree', self.degrees_iter)
        

    def create_index_unseen_degree(self):

        self.index_parameter_generic('unseen_degree', self.degrees_iter)
        

    def remove_degree_cache(self):

        self.remove_parameter_cache('degree')
        

    def create_index_clustering(self):
        
        self.index_parameter_generic('clustering', self.clustering_indices_iter)

        
    def create_index_triangles(self):
        
        self.index_parameter_generic('triangles', self.triangles_iter)

        
    def create_index_knn(self):

        self.index_parameter_generic('knn', self.average_neighbor_degrees_iter)
        
        
    def create_index_kcores(self):

        self.find_cores()        
        
        
    def index_parameter_generic(self, param_name, param_iter_func):
        
        self.add_parameter_cache(param_name)
        
        modulo = 1000
        estimator = TimeEstimator(self.number_of_nodes()/modulo)
        count = 1
        for node, value in izip( self.nodes_iter(), param_iter_func(),):
            
            if self.debug and count%modulo == 0:
                print 'INFO: %d nodes processed in index_parameter_generic, param_name %s' % (count, param_name)
                estimator.tick()
                print estimator.log_line()
            
            self.insert_parameter_cache(param_name, node, value)
            count +=1
        
        self.index_parameter_cache(param_name)
        
              
    def initialize_parameter(self, param_name, value=0.0):
        
        for node in self.nodes_iter():
            
            self.insert_parameter_cache(param_name, node, value)
        
              
    def index_parameter_from_degree(self, param_name):
        
        self.add_parameter_cache(param_name)
        
        query = '''
        insert into parameter_%s
        select 
            nodes.id, count(*)
        from 
            nodes, edges
        where 
            nodes.id = edges.src
        group by nodes.id  
        ''' % param_name

        self.conn.cursor().execute(query)
        
        self.index_parameter_cache(param_name)
        
              
    def index_parameter_from_parameter(self, param_src, param_dst, ):
        
        self.add_parameter_cache(param_dst)
        
        query = '''
        insert into parameter_%s
        select *
        from parameter_%s
        ''' % (param_dst, param_src)

        self.conn.cursor().execute(query)
        
        self.index_parameter_cache(param_dst)
        
              
    def create_index_linksphere(self, lookahead):

        self.index_parameter_generic('linksphere%d'%lookahead, lambda : self.linksphere_iter(None, lookahead) )
        

    def create_index_nodesphere(self, lookahead):

        self.index_parameter_generic('nodesphere%d'%lookahead, lambda : self.nodesphere_iter(None, lookahead) )
        

    def __del__(self):
        
        if not self.persistant:
            os.remove( self.__filename )
    

    def erase_from_disk(self):
        
        if self.persistant:
            os.remove( self.__filename )
    

    def add_node(self, node):
        
        if not self.has_node(node):
            c = self.conn.cursor()
            c.execute("insert into nodes (node) values (?)", (str(node),) )
        
        
    def number_of_nodes(self):
        query = '''
        select count(*) 
        from nodes
        '''
        ret = None            
        for row in self.conn.cursor().execute(query):
            ret = row[0]
        return ret
    
                
    def has_node(self, node):
        ret = False
        for _ in self.conn.cursor().execute("select * from nodes where node=?", (str(node),) ):
            ret = True
            break
        return ret
            
        
    def nodes(self):
        raise BigGraphException('Error: nodes() not implemented, use nodes_iter() !!!')


    def nodes_iter(self):
        for row in self.conn.cursor().execute("select node from nodes ORDER BY nodes.node"):
            yield row[0]
        
    
    def node_id(self, node):
        ret = None
        for row in self.conn.cursor().execute("select id from nodes where node=?", (str(node),) ):
            ret = row[0]
            break
        return ret
    
    
    def add_edge(self, src, dst, weight=1):
        
	#print src, dst

        self.add_node(src)
        src_id = self.node_id(src)
        
        self.add_node(dst)
        dst_id = self.node_id(dst)
        
        c = self.conn.cursor()
        try:        
            # Insert a boths links
            c.execute("""insert into edges              
              values (?, ?, ?)""", (src_id, dst_id, weight))
              #values (?, ?)""", (src_id, dst_id))
            c.execute("""insert into edges
              values (?, ?, ?)""", (dst_id, src_id, weight))
              #values (?, ?)""", (dst_id, src_id))              
        except sql.IntegrityError:
            pass
        

    def update_edge_weight(self, src, dst, weight):
        
        self.add_node(src)
        src_id = self.node_id(src)
        
        self.add_node(dst)
        dst_id = self.node_id(dst)
        
        c = self.conn.cursor()
        
        # Insert a boths links
        c.execute("""update edges
                     set weight = ?
                     where src = ? and dst = ?  
          """, (weight, src_id, dst_id, ))
        c.execute("""update edges
                     set weight = ?
                     where src = ? and dst = ?  
          """, (weight, dst_id, src_id,  ))
            

    def has_edge(self, node1, node2):
        ret = False
                    
        query = '''
        select nodes1.node, nodes2.node 
        from nodes as nodes1, nodes as nodes2
        join edges
        where nodes1.id = edges.src and nodes2.id = edges.dst 
        and nodes1.node = ? and nodes2.node = ?
        '''
        for _ in self.conn.cursor().execute(query, (str(node1),str(node2),) ):
            ret = True
            break
        return ret
            
        
    def edge_weight(self, node1, node2):
        ret = None
                    
        query = '''
        select edges.weight 
        from nodes as nodes1, nodes as nodes2
        join edges
        where nodes1.id = edges.src and nodes2.id = edges.dst 
        and nodes1.node = ? and nodes2.node = ?
        '''
        for r in self.conn.cursor().execute(query, (str(node1),str(node2),) ):
            ret = r[0] 
            break
        return ret
            
        
    def number_of_edges(self):
        query = '''
        select count(*) / 2
        from edges
        '''
        ret = None            
        for row in self.conn.cursor().execute(query):
            ret = row[0]
        return ret
    
                
    def edges(self, nbunch=None ):
        raise BigGraphException('Error: edges() not implemented, use edges_iter() !!!')


    def edges_iter(self, nbunch=None, upper_bound_weigh=1):
        
        if not nbunch:
            query = '''
            select distinct nodes1.node, nodes2.node 
            from nodes as nodes1, nodes as nodes2
            join edges
            where nodes1.id = edges.src and nodes2.id = edges.dst 
                and nodes1.id <= nodes2.id and edges.weight <= ?
            '''            
            for row in self.conn.cursor().execute(query, (upper_bound_weigh,)):
                    yield row[0], row[1]       
    
        else:
            
            query = '''
            select nodes1.node, nodes2.node, edges.weight 
            from nodes as nodes1, nodes as nodes2
            join edges
            where nodes1.id = edges.src and nodes2.id = edges.dst and nodes1.node = ?
            and edges.weight <= ?                
            '''
            
            if isinstance(nbunch, int) or isinstance(nbunch, str):
                nbunch = [nbunch]
                
            for node in nbunch:
                for row in self.conn.cursor().execute(query, (str(node),upper_bound_weigh,)):
                    #if row[2] <= upper_bound_weigh:
                        yield row[0], row[1]    

            
    def degrees(self, nodes=None):
        raise BigGraphException('Error: degrees() not implemented, use degrees_iter() !!!')        

    
    def degrees_iter(self, nodes=None):
        return self.generic_networkx_parameter_iter(self.__degree, 'degrees', None, nodes)


    def degree(self, node, lower_bound_weight=1 ):
        return self.__degree(self, node, lower_bound_weight)        
        

    def __degree(self, big_graph, node, lower_bound_weight=1):
        
        query = '''
        select 
            count(*)
        from 
            nodes, edges
        where 
            nodes.node = ? and nodes.id = edges.src and edges.weight >= ?
        '''

        ret = None
        for r in big_graph.conn.cursor().execute(query, (str(node), lower_bound_weight,)):
            ret = r[0] 
        return ret

            
    def clustering_indices_iter(self, nodes=None):        
        return self.generic_networkx_parameter_iter(self.__clustering, 'clustering_indices', None, nodes)

    
    def clustering_indices(self, nodes=None):        
        raise BigGraphException('Error: clustering_indices() not implemented, use clustering_indices_iter() !!!')        


    def clustering(self, node ):
        return self.__clustering(self, node)        
        

    def __clustering(self, big_graph, node):

        ret = self.__triangles(big_graph, node)

        #print ret
        
        degree = self.degree(node)
        if degree <= 1:
            return 0.0
        return float(ret)*2.0 / (degree*(degree-1))

            
    def neighbors(self, node):
        
        neighs = []
        for _, neigh in self.edges_iter([node]):
            neighs.append (  neigh )
        return neighs
    

    def neighbors_iter(self, node, upper_bound_weigh=1):
        
        for _, neigh in self.edges_iter([node], upper_bound_weigh):
            yield neigh
    

    def check_parameter_name(self, parameter_name):

        # check that the parameter name is ok
        findings = re.findall('[a-z_]+[a-z_0-9]*', parameter_name)
        if len(findings)==0 or len(findings[0]) != len(parameter_name):
            raise BigGraphException('Error: bad parameter name, only [a-z_]+ allowed!') 
        
    
    def add_parameter_cache(self, parameter_name):

        self.check_parameter_name(parameter_name)
                
        #try:
        c = self.conn.cursor()
        # Create table for nodes
        
        #c.execute('''create table if not exists parameter_%s 
        #            (node_id integer primary key, value real)''' % parameter_name)
        c.execute('''create table parameter_%s 
                    (node_id integer primary key, value real)''' % parameter_name)
        
        #except sql.OperationalError: # only create tables the first time
        #    pass
    
    
    def has_parameter_cache(self, parameter_name):
    
        try:
            self.add_parameter_cache(parameter_name)
            ret = False
            self.remove_parameter_cache(parameter_name)
        except: # already existing
            ret = True            
        return ret

    
    def remove_parameter_cache(self, parameter_name):

        self.check_parameter_name(parameter_name)
                
        try:
            c = self.conn.cursor()
            # Create table for nodes
            c.execute('''drop table if exists parameter_%s''' % parameter_name)
        except sql.OperationalError: # only create tables the first time
            pass
    
    
    def index_parameter_cache(self, parameter_name):

        self.check_parameter_name(parameter_name)
                
        try:
            c = self.conn.cursor()
            # Create index for nodes
            c.execute('''create index if not exists 
                    parameter_%s_index on parameter_%s (value)''' % (parameter_name,parameter_name) )
        except sql.OperationalError: # only create tables the first time
            pass
    
    
    def remove_index_parameter_cache(self, parameter_name):

        self.check_parameter_name(parameter_name)
                
        try:
            c = self.conn.cursor()
            # Create index for nodes
            c.execute('''drop index if exists parameter_%s_index''' % (parameter_name) )
        except sql.OperationalError: # only create tables the first time
            pass
    
    
    def check_node(self, node):

        if not self.has_node(node):
            raise BigGraphException('Error: node %s not in BigGraph instance!' % str(node) )
    
    
    def check_float(self, value):
        
        try:
            return float(value)
        except:
            raise BigGraphException('Error: value %s is not a floating-point or equivalent number!' % str(value))
        
    
    def insert_parameter_cache(self, param_name, node, value):
        
        #self.check_parameter_name(param_name)
        #self.check_node(node)
        value = self.check_float(value)
        
        # Create index for nodes
        query = '''insert into parameter_%s
                   select id, ? from nodes where node = ?
                ''' % (param_name)
        try:
            self.conn.cursor().execute(query, (value, str(node), ))
        except sql.IntegrityError:
            raise BigGraphException('Error: duplicate insertion of parameter %s, node %s value %s' % (param_name, node, value))

    
    def update_parameter_cache(self, param_name, node, value):
        '''
        
        '''
        
        #self.check_parameter_name(param_name)
        #self.check_node(node)
        value = self.check_float(value)

        if not self.has_node(node):
            raise BigGraphException('Error: node %s not in BigGraph instance!' % str(node) )
        
        # Create index for nodes
        query = '''update parameter_%s
                   set value = ?
                   where node_id in (select id from nodes where node = ?)
                ''' % (param_name)
            
        self.conn.cursor().execute(query, (value, str(node), ))

    
    def dec_parameter_cache(self, param_name, node):
        
        #self.check_parameter_name(param_name)
        #self.check_node(node)

        #if not self.has_node(node):
        #    raise BigGraphException('Error: node %s not in BigGraph instance!' % str(node) )
        
        # Create index for nodes
        query = '''update parameter_%s
                   set value = max(0.0, value - 1.0) 
                   where node_id in (select id from nodes where node = ?)
                ''' % (param_name)
            
        self.conn.cursor().execute(query, (str(node), ))

    
    def inc_parameter_cache(self, param_name, node):
        
        #self.check_parameter_name(param_name)
        #self.check_node(node)

        #if not self.has_node(node):
        #    raise BigGraphException('Error: node %s not in BigGraph instance!' % str(node) )
        
        # Create index for nodes
        query = '''update parameter_%s
                   set value = value + 1.0 
                   where node_id in (select id from nodes where node = ?)
                ''' % (param_name)
            
        self.conn.cursor().execute(query, (str(node), ))

    
    def get_parameter_cache(self, param_name, node):
        
        #self.check_parameter_name(param_name)
        #self.check_node(node)
                
        # Create index for nodes
        query = '''select param.value
                    from parameter_%s as param
                    join nodes
                    where param.node_id = nodes.id
                    and nodes.node = ?
                ''' % (param_name)

        value = None
        for row in self.conn.cursor().execute(query, (str(node),)):
            value = row[0]
        return value    
        
    
    def get_max_value_parameter_cache(self, param_name):
        
        # Create index for nodes
        query = '''select max(param.value)
                    from parameter_%s as param
                ''' % (param_name)

        value = None
        for row in self.conn.cursor().execute(query):
            value = row[0]
        return value    
        
    
    def get_sum_value_parameter_cache(self, param_name):
        
        # Create index for nodes
        query = '''select sum(param.value)
                    from parameter_%s as param
                ''' % (param_name)

        value = None
        for row in self.conn.cursor().execute(query):
            value = row[0]
        return value    
        
    
    def get_parameter_cache_inverse(self, param_name, value):
        
        #self.check_parameter_name(param_name)
        #value = self.check_float(value)

        query = '''select nodes.node
                    from nodes
                    join parameter_%s as param
                    where nodes.id = param.node_id 
                    and (param.value between ? / 1.001 and ? / 0.999)    
                    order by random()
                ''' % (param_name) # and param.value = ?

        for row in self.conn.cursor().execute(query, (float(value),float(value),)):
            yield row[0]
        
    
    def get_parameter_cache_inverse_orderby(self, param_name, value, param_name_orderby, ascending=False):
        
        if ascending:
            order = 'param_orderby.value asc'
        else:
            order = 'param_orderby.value desc'

        query = '''select nodes.node
                    from nodes, parameter_%s as param, parameter_%s as param_orderby
                    where nodes.id = param.node_id and param_orderby.node_id = param.node_id
                    and (param.value between ? / 1.001 and ? / 0.999)    
                    order by %s
                ''' % (param_name, param_name_orderby, order) # and param.value = ?

        for row in self.conn.cursor().execute(query, (float(value),float(value),)):
            yield row[0]
        
    
    def get_parameter_cache_inverse_between(self, param_name, lower, upper):
        
        #self.check_parameter_name(param_name)
        #value = self.check_float(value)

        query = '''select nodes.node
                    from nodes
                    join parameter_%s as param
                    where nodes.id = param.node_id 
                    and (param.value between ? and ?)    
                ''' % (param_name) # and param.value = ?

        for row in self.conn.cursor().execute(query, (float(lower),float(upper),)):
            yield row[0]
        
    
    def get_parameter_cache_inverse_count(self, param_name, value):
        
        self.check_parameter_name(param_name)
        value = self.check_float(value)

        query = '''select count(*)
                    from nodes
                    join parameter_%s as param
                    where nodes.id = param.node_id 
                    and (param.value between ? / 1.001 and ? / 0.999)    
                ''' % (param_name) # and param.value = ?

        ret = None
        for row in self.conn.cursor().execute(query, (value,value,)):
            ret = row[0]
            break
        return ret
        
    
    def get_parameter_cache_inverse_count_gt(self, param_name, value):
        
        self.check_parameter_name(param_name)
        value = self.check_float(value)

        query = '''select count(*)
                    from nodes
                    join parameter_%s as param
                    where nodes.id = param.node_id 
                    and (param.value > ? )    
                ''' % (param_name) # and param.value = ?

        ret = None
        for row in self.conn.cursor().execute(query, (value,)):
            ret = row[0]
            break
        return ret
        
    
    def get_parameter_cache_inverse_gt(self, param_name, value, ascending=False, random=False):
        
        self.check_parameter_name(param_name)
        value = self.check_float(value)

        if not random:
            if ascending:
                order = 'param.value asc'
            else:
                order = 'param.value desc'
        else:
            order = 'random()'

        query = '''select nodes.node
                    from nodes
                    join parameter_%s as param
                    where nodes.id = param.node_id 
                    and (param.value > ? )
                    order by %s    
                ''' % (param_name, order) # and param.value = ?

        ret = None
        for row in self.conn.cursor().execute(query, (value,)):
            yield row[0]
        
    
    def get_parameter_cache_inverse_count_lt(self, param_name, value):
        
        self.check_parameter_name(param_name)
        value = self.check_float(value)

        query = '''select count(*)
                    from nodes
                    join parameter_%s as param
                    where nodes.id = param.node_id 
                    and (param.value < ? )    
                ''' % (param_name) # and param.value = ?

        ret = None
        for row in self.conn.cursor().execute(query, (value,)):
            ret = row[0]
            break
        return ret
        
    
    def get_parameter_cache_iter(self, param_name, random=False, ascending=False):    

        self.check_parameter_name(param_name)

        if not random:
            if ascending:
                order = 'param.value asc'
            else:
                order = 'param.value desc'
        else:
            order = 'random()'
            
        query = '''select nodes.node, param.value
                    from parameter_%s as param
                    join nodes
                    where param.node_id = nodes.id
                    order by %s
                ''' % (param_name, order)

        for row in self.conn.cursor().execute(query):
            yield row[0], row[1]

    
    def lookahead_edges(self, nbunch, lookahead):
        raise BigGraphException('Error: lookahead_edges() not implemented in BigGraph, use lookahead_edges_iter() instead!!!')        


    def lookahead_edges_iter(self, nbunch, lookahead):

        nbunch_iter = (n for n in nbunch if self.has_node(n))        
        edge_bunch_list = [self.edges_iter(nbunch_iter)]
        
        for _ in range(lookahead - 1):
            new_nodes = [d for _, d in edge_bunch_list[-1]]
            edge_bunch_list.append(self.edges(new_nodes))
            
        ret = set([])
        for edge_set in edge_bunch_list:
            ret = ret.union(edge_set)
        return ret


    def reset_edge_weights(self):
        
        query = '''update edges
                   set weight = 1
                '''
            
        self.conn.cursor().execute(query)    


    def linksphere_iter(self, nodes=None, lookahead=1):
        return self.generic_networkx_parameter_iter(lambda self, node : self.count_edges_lookahead(node, lookahead), 'linksphere%d'%lookahead, None, nodes)


    def edges_lookahead_recursive(self, node, lookahead):    

        edges = [((v<w and v or w), (v<w and w or v)) for v,w in list(self.edges_iter([node]))]
        if lookahead == 0:
            return edges        
        
        for neigh in self.neighbors_iter(node):
            
            edges += self.edges_lookahead_recursive(neigh, lookahead-1)

        return edges


    def count_edges_lookahead(self, node, lookahead):    

        return len(set(self.edges_lookahead(node, lookahead) ))
    
    
    def count_nodes_lookahead(self, node, lookahead):    

        edges = self.edges_lookahead(node, lookahead)
        return len(set( [v for v,_ in edges] + [w for _,w in edges] ))
    
    
    def edges_lookahead(self, node, lookahead):    
        
        edges = [((v<w and v or w), (v<w and w or v)) for v,w in list(self.edges_iter([node]))]
        visited = set([node])
        new_nodes = list(self.neighbors_iter(node))
        for _ in range(lookahead):
            
            copy_new_nodes = new_nodes
            new_nodes = []
            for new_node in copy_new_nodes:
                
                visited.add( new_node )
                for new_node_neigh in self.neighbors_iter(new_node):
                    
                    if not new_node_neigh in visited:
                        new_nodes.append( new_node_neigh )
                        edges.append( (lambda v,w: ((v<w and v or w), (v<w and w or v))) (new_node, new_node_neigh) )
                
            new_nodes = list(set(new_nodes))
            
        #print edges
   
        return edges
             

        #edges = self.edges_lookahead_recursive(node, lookahead)
        
        #print edges

        #return len(set(edges))            
            

#        query = self.__count_edges_lookahead_query(lookahead)
#
#        ret = None
#        #sql_params = tuple([node]*(2**lookahead))
#        sql_params = tuple([node]) * 2**lookahead
#        #count = 0
#        for row in self.conn.cursor().execute(query, sql_params):
#            ret = row[0]
#            #count += 1
#            break
#        return ret


    def __count_edges_lookahead_query(self, lookahead):
        
        q = '''select distinct src, dst from (
                    select src, dst
                    from edges, nodes
                    where node = ? and (src = id or dst = id )
                    )
            '''
        
        for _ in range(lookahead):
            q = '''select src, dst
                    from edges
                    where src in (select dst from (%s))
                ''' % (q)
                
        q += ''

        q = 'select count(*)/2 from (%s)' % q
        
        return q
        
        
#    def edges_lookahead(self, node, lookahead):
#        
#        query = self.__edges_lookahead_query(lookahead)
#
#        ret = None
#        sql_params = tuple([node]*(2**lookahead))
#        #sql_params = tuple([node]) * 2**lookahead
#        #count = 0
#        for row in self.conn.cursor().execute(query, sql_params):
#            yield row
#            #count += 1
       

    def __edges_lookahead_query(self, lookahead):
        
        q = '''select distinct src, dst from (
                    select src, dst
                    from edges, nodes
                    where node = ? and (src = id or dst = id)
                    )
            '''
        
        for _ in range(lookahead):
            q = '''select src, dst
                    from edges
                    where src in (select dst from (%s))
                   union
                   select src, dst
                    from edges
                    where dst in (select dst from (%s))                    
                ''' % (q,q)
                
        q += ''
                
            
        return q
        

    def nodesphere_iter(self, nodes=None, lookahead=1):
        return self.generic_networkx_parameter_iter(lambda self, node : self.count_nodes_lookahead(node, lookahead), 'nodesphere%d'%lookahead, None, nodes)


#    def count_nodes_lookahead(self, node, lookahead):    
#
#        query = self.__count_nodes_lookahead_query(lookahead)
#
#        ret = None
#        sql_params = tuple([node]*(2**lookahead))
#        #count = 0
#        for row in self.conn.cursor().execute(query, sql_params):
#            ret = row[0]
#            #count += 1
#            break
#        return ret


    def __count_nodes_lookahead_query(self, lookahead):
        
        # weight 1 means unvisited edge
        q = '''select distinct dst from (
                    select src, dst
                    from edges, nodes
                    where node = ? and src = id and src < dst
            '''
        
        for _ in range(lookahead):
            q += '''union
                    select src, dst
                    from edges
                    where src < dst and src in (select dst from (%s)))                    
                ''' % q
                
        q += ')'

        q = 'select count(*)+1 from (%s)' % q
        
        return q
        



#    def __edges_lookahead_query(self, lookahead):
#        
#        # weight 1 means unvisited edge
#        q = '''select distinct src, dst, edge_id from (
#                    select src, dst, edge_id
#                    from edges, nodes
#                    where node = ? and src = id and weight = 1 and src < dst
#            '''
#        
#        for _ in range(lookahead):
#            q += '''union
#                    select src, dst, edge_id
#                    from edges
#                    where weight = 1 and src < dst and src in (select dst from (%s)))                    
#                ''' % q
#                
#        q += ')'
#        
#        return q
        

    def update_neighborhood_lookahead(self, node, lookahead):

        # mark edges as visited
        q_visited = '''update edges
                        set weight = max(0, weight - 1) 
                        where edge_id in (select count(edge_id) from (%s))  
                    ''' % self.__edges_lookahead_query(lookahead)
                    #where edges.src, edges.dst in (%s)

        sql_params = tuple([node]*(2**lookahead))

        self.conn.cursor().execute(q_visited, sql_params)
        
        
    def dec_neighbors_parameter(self, node, param):

        query = '''update parameter_%s
                   set value = max(0.0, value - 1.0) 
                   where node_id in (
                    select edges.dst 
                    from nodes
                    join edges
                    where nodes.node = ? 
                      and nodes.id = edges.src                    
                      and edges.src <= edges.dst
                    )
                ''' % (param)
            
        self.conn.cursor().execute(query, (str(node), ))


    
    def dec_neighborhood_parameter(self, node, lookahead, param):

        sql_params = tuple([node]*(2**lookahead * 2))

        q_unseen_degree = '''update parameter_%s
                        set value = max(0.0, value - (select count(%s) from (%s) where %s=node_id) ) 
                        where node_id in (select %s from (%s))
                    ''' 

#        print '-'*60
#        for n, val in self.get_parameter_cache_iter('unseen_degree'):
#            print n, val

        # decrease for source node
        q = q_unseen_degree % (param, 'src',self.__edges_lookahead_query(lookahead),'src','src',self.__edges_lookahead_query(lookahead))
        self.conn.cursor().execute(
                                   q,
                                   sql_params,
                                   )
        
#        print '-'*60
#        for n, val in self.get_parameter_cache_iter('unseen_degree'):
#            print n, val
            
        # decrease for destination node        
        q = q_unseen_degree % (param, 'dst',self.__edges_lookahead_query(lookahead),'dst','dst',self.__edges_lookahead_query(lookahead))
        self.conn.cursor().execute(
                                   q,
                                   sql_params,
                                   )
        
#        print '-'*60
#        for n, val in self.get_parameter_cache_iter('unseen_degree'):
#            print n, val
        pass


    def edges_neighborhood(self, node, lookahead):

        
        sql_params = tuple([node]*(2**lookahead))
        
        q = '''select node1.node, node2.node 
                from nodes as node1, nodes as node2, (%s)
                where node1.id = src and node2.id = dst
                ''' % self.__edges_lookahead_query(lookahead)
        for row in self.conn.cursor().execute(q, sql_params):
            yield row[0], row[1]


    def kcoreness(self, nodes=None):        
        raise BigGraphException('Error: kcoreness() not implemented, use kcoreness_iter() !!!')
    
    
    def kcoreness_iter(self, nodes=None):        
        if not self.has_parameter('shell'):        
            self.cores = self.find_cores()
        kcoreness_func = lambda big_graph, node: int(big_graph.get_parameter_cache('shell', node))
        return self.generic_networkx_parameter_iter(kcoreness_func, 'kcoreness', None, nodes)


    def find_cores(self):
        """Return the core number for each vertex.
    
        See: arXiv:cs.DS/0310049 by Batagelj and Zaversnik
            
        A table of the coreness k-shell numbers is filled under parameter name 'shell'.
        """

        try:
            self.create_index_degree()
        except:
            pass
        
        shell = 'shell'
        self.remove_parameter_cache(shell)
        self.index_parameter_from_degree(shell) # build table with degrees

        visited = 'visited'
        self.remove_parameter_cache(visited)
        self.index_parameter_from_parameter(shell, visited) # quick copy of table

        
        self.__max_count = self.number_of_nodes()
        self.__count = 0
        if self.debug:
            print 'INFO: BEGIN update_shell_recursive() total of %d nodes ...' % (self.__max_count)

        max_degree = self.get_max_value_parameter_cache(shell)
        for d in range(int(max_degree)+1):
            
            non_empty_degree = True 
            while non_empty_degree:
            
                non_empty_degree = False
                # get unvisited nodes of partial degree d
                for node in self.get_parameter_cache_inverse(visited, d):

                    non_empty_degree = True

                    if self.debug and self.__count%10000 == 0:
                        print 'INFO: BEGIN update_shell_recursive() %d nodes of a total of %d nodes ...' % (self.__count, self.__max_count)
                        self.__count += 1
                    
                    self.update_parameter_cache(visited, node, -1.0) # mark as visited
    
                    for neigh in self.neighbors_iter(node):            
            
                        neigh_shell = self.get_parameter_cache(visited, neigh)
                        
                        if neigh_shell < 0: # if visited
                            continue
                        
                        if neigh_shell == d: # if in the same shell
                            continue
                        
                        self.dec_parameter_cache(visited, neigh)
                        self.dec_parameter_cache(shell, neigh)
                    
        self.remove_parameter_cache('visited')        

        if self.debug:
            print 'INFO: END update_shell_recursive() total of %d nodes ...' % (self.__max_count)
                   
        
    def find_cores2(self):
        """Return the core number for each vertex. Recursive algorithm (danger!).
    
        See: arXiv:cs.DS/0310049 by Batagelj and Zaversnik
            
        A table of the coreness k-shell numbers is filled under parameter name 'shell'.
        """

        try:
            self.create_index_degree()
        except:
            pass
        
        shell = 'shell'
        self.remove_parameter_cache(shell)
        self.index_parameter_from_degree(shell)

        max_degree = self.get_max_value_parameter_cache(shell)
        
        self.__max_count = self.number_of_nodes()
        self.__count = 0
        if self.debug:
            print 'INFO: BEGIN update_shell_recursive() total of %d nodes ...' % (self.__total_count)

        self.add_parameter_cache('visited')
        self.initialize_parameter('visited')
        degree = 0
        for degree in range(int(max_degree)+1):
            
            for v in self.get_parameter_cache_inverse(shell, degree):
                
                self.update_shell_recursive(v, degree)
    
        self.remove_parameter_cache('visited')        

        if self.debug:
            print 'INFO: END update_shell_recursive() total of %d nodes ...' % (self.__total_count)
                   
        
    def update_shell_recursive(self, node, degree):

        if self.get_parameter_cache('visited', node) > 0: # if visited
            return

        if self.debug :
            if self.__count % 10000 == 0:
                print 'INFO: update_shell_recursive() %d nodes from a total of %d nodes  %s ...' % (self.__count, self.__total_count, time.ctime())
            self.__count += 1

        self.update_parameter_cache('visited', node, 1.0) # mark as visited

        
        for neigh in self.neighbors_iter(node):            

            if self.get_parameter_cache('visited', neigh) > 0: # if visited
                continue
            
            self.dec_parameter_cache('shell', neigh)
            
            if self.get_parameter_cache('shell', neigh) <= degree:
                
                self.update_shell_recursive(neigh, degree)
                

    def remove_edge(self, src, dst): 

        src_id = self.node_id(src)
        dst_id = self.node_id(dst)
        if not src_id or not dst_id:
            raise BigGraphException("The edge %s-%s is not in the graph"%(str(u),str(v)))
        
        c = self.conn.cursor()

        # remove both directions
        c.execute("""delete from edges
          where src = ? and dst = ?""", (src_id, dst_id))
        c.execute("""delete from edges
          where src = ? and dst = ?""", (dst_id, src_id))
        

    def has_parameter(self, param_name):
        
        ret = False
        try:
            self.add_parameter_cache(param_name)
            self.remove_parameter_cache(param_name)            
        except sql.OperationalError: # only create tables the first time
            ret = True
            
        return ret
    
    
    def total_triangles(self):

        if self.has_parameter_cache('triangles'):
            return self.get_sum_value_parameter_cache('triangles') / 3.0
        else:
            raise BigGraphException('triangles not indexed!')
        
#        query = '''
#        select 
#            count(*)
#        from 
#            edges as edges1, edges as edges2, edges as edges3
#        where 
#            edges1.src < edges1.dst
#        and
#            edges2.src < edges2.dst
#        and
#            edges1.dst = edges2.src 
#        and 
#            edges2.dst = edges3.src 
#        and 
#            edges3.dst = edges1.src 
#        '''
#        
#        ret = None
#        for row in self.conn.cursor().execute(query):
#            ret = row[0]            
#        
#        return ret
        
        
    def total_triangles_weight(self, weight=1):
        
        query = '''
        select 
            count(*) / 6
        from 
            edges as edges1, edges as edges2, edges as edges3
        where
            edges1.weight = %d
        and
            edges2.weight = %d
        and
            edges3.weight = %d
        and
            edges1.dst = edges2.src 
        and 
            edges2.dst = edges3.src 
        and 
            edges3.dst = edges1.src 
        ''' % (weight,weight,weight,)
        
        ret = None
        for row in self.conn.cursor().execute(query):
            ret = row[0]            
        
        return ret
        
        
    def __triangles(self, big_graph, node):    
        
        query = '''
        select 
            count(*) / 2
        from 
            nodes, edges as edges1, edges as edges2, edges as edges3
        where 
            edges1.dst = edges2.src 
        and 
            edges2.dst = edges3.src 
        and 
            edges3.dst = edges1.src 
        and
            nodes.id = edges1.src
        and
            nodes.node = ?        
        '''
        
        ret = None
        for row in big_graph.conn.cursor().execute(query, (str(node),)):
            ret = row[0]            
        
        return ret


    def triangles_iter(self, nodes=None):        
        return self.generic_networkx_parameter_iter(self.__triangles, 'triangles', None, nodes)

    
    def triangles(self, nodes=None):        
        return self.generic_networkx_parameter(self.__triangles, 'triangles', None, nodes)

    
    def total_unseen_triangles(self):

        if self.has_parameter_cache('unseen_triangles'):
            return self.get_sum_value_parameter_cache('unseen_triangles') / 3.0
        else:
            raise BigGraphException('unseen_triangles not indexed!')
        
        
    def triangles_weight(self, node, weight=1):
        '''
        1 == not visible yet
        2 == visible 
        '''
        
        query = '''
        select 
            count(*) / 2
        from 
            nodes, edges as edges1, edges as edges2, edges as edges3
        where
            edges1.weight = %d
        and
            edges2.weight = %d
        and
            edges3.weight = %d
        and
            edges1.dst = edges2.src 
        and 
            edges2.dst = edges3.src 
        and 
            edges3.dst = edges1.src 
        and
            nodes.id = edges1.src
        and
            nodes.node = ?        
        ''' % (weight,weight,weight,)
        
        ret = None
        for row in self.conn.cursor().execute(query, (str(node),)):
            ret = row[0]            
        
        return ret
            

    def total_seen_triangles(self):

        if self.has_parameter_cache('seen_triangles'):
            return self.get_sum_value_parameter_cache('seen_triangles') / 3.0
        else:
            raise BigGraphException('seen_triangles not indexed!')
        
        
    def __iter__(self):
        return self.nodes_iter()
    
    
    def __getitem__(self, n):
        """Return a dict of neighbors of node n.  Use the expression 'G[n]'.

        Parameters
        ----------
        n : node
           A node in the graph.

        Returns
        -------
        adj_dict : dictionary
           The adjacency dictionary for nodes connected to n.

        Notes
        -----
        G[n] is similar to G.neighbors(n) but the internal data dictionary
        is returned instead of a list.

        Assigning G[n] will corrupt the internal graph data structure.
        Use G[n] for reading data only.

        Examples
        --------
        >>> G = nx.Graph()   # or DiGraph, MultiGraph, MultiDiGraph, etc
        >>> G.add_path([0,1,2,3])
        >>> print G[0]
        {1: {}}
        """        
        return dict( [(k,{}) for k in self.neighbors_iter(n)]  )        


    def __contains__(self, n):
        return self.has_node(n)
    

    def add_edges_from(self, ebunch):
        module = 10000
        count = 0
        for src, dst in ebunch:
            if not self.edge_weight(src, dst) == 2:
                self.update_edge_weight(src, dst, 2)
                self.add_edge(src, dst)
                if count % module == 0:
                    print 'added %d edges %s ... ' % (count, time.ctime())
                count += 1    
        

    
    def save_snowball_edgelist_iter(self, filename):
        
        out = open(filename, 'w')

        self.remove_parameter_cache('visited')
        self.add_parameter_cache('visited')
        self.initialize_parameter('visited', 100000000) # 100000000 = not visited
        self.index_parameter_cache('visited')

        # TODO: no usar tiempo, es missleading y dificil de dbugearr, usar un contador!!!
        count = 0

        modulo = 10000
        total = self.number_of_edges()
        estimator = TimeEstimator(total/modulo)
        count = 0
        
        for n, val in self.get_parameter_cache_iter('visited'):
            node, visited = n, val
            break
        
        visited = 0
        self.update_parameter_cache('visited', node, visited) # < 0 means not visited
        while visited  <= 100000000.0:

            # 
            for n, val in self.get_parameter_cache_iter('visited', random=False, ascending=True):
                node, visited = n, val
                break
            if visited == 100000001.0 or visited == 100000000.0:
                break # finish connected (100000001.0) or disconnected (100000000.0) graph!
            self.update_parameter_cache('visited', node, 100000001) # 100000001 = visited   
            
            for neigh in self.neighbors_iter(node):
                
                if self.get_parameter_cache('visited', neigh) <= 100000000: # not visited

                    count += 1
                    self.update_parameter_cache('visited', neigh, count)
        
                    out.write('%s %s\n' % (str(node),str(neigh)))

                    if self.debug and count%modulo == 0:
                        print 'INFO: %d edges dumped in save_snowball_edgelist_big(), total %d' % (count, total)
                        estimator.tick()
                        print estimator.log_line()

                
        self.remove_parameter_cache('visited')


                
        
        
if __name__ == '__main__':
    
    g = BigGraph('/tesis/lj-100k.big_graph')
    g.debug = True
    g.save_snowball_edgelist('/tesis/lj-snowball.txt')
    
