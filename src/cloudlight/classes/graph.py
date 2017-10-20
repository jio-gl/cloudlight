'''
Created on Mar 16, 2010

@author: jose
'''

import sys, zlib, base64, time, re, cPickle, copy
from math import log
from random import shuffle
from cStringIO import StringIO

import networkx as nx

from cloudlight.utils.random_items import random_items
from cloudlight.utils.itertools_recipes import izip
from cloudlight.utils.misc import Base, identity
from cloudlight.utils.estimator import TimeEstimator
# matplot lib is an OPTIONAL dependency.
try:
    import matplotlib.pyplot as plt
except:
    pass


class GraphException(Exception):
    pass


class IndexedTable:
    
    def __init__(self):
        
        self.__rep = {}
        self.__rep_inv = {}

    
    def __contains__(self, key):
        return key in self.__rep
    
    
    def __len__(self):
        return len(self.__rep)


    def __setitem__(self, key, item):
        
        if key in self.__rep:
            self.__rep_inv[self.__rep[key]].remove( key )
            if len(self.__rep_inv[self.__rep[key]]) == 0:
                del self.__rep_inv[self.__rep[key]]
            del self.__rep[key]
            
        self.__rep[key] = item
        
        if not item in self.__rep_inv:
            self.__rep_inv[item] = set([])
        self.__rep_inv[item].add( key )


    def __getitem__(self, key):

        return self.__rep[key]


    def keys(self):
        return self.__rep.keys()
    

    def items(self):
        return self.__rep_inv.keys()
    

    def preimage(self, item):
        
        if item in self.__rep_inv:
            for key in self.__rep_inv[item]:
                yield key


    def preimage_size(self, item):
        
        return item in self.__rep_inv and len( self.__rep_inv[item] ) or 0


    def iterate(self, random=False, ascending=False):
        
        if random:
            
            keys = list(self.__rep.keys())
            shuffle(keys)
            
            for key in keys:
                yield key, self.__rep[key]
            
        else:
            
            items = list(self.__rep_inv.keys())
            
            if ascending:
                items.sort(cmp=None, key=None, reverse=False)
            else:
                items.sort(cmp=None, key=None, reverse=True)

            for item in items:
                for key in self.__rep_inv[item]:
                    yield key, item


class Graph(nx.Graph):
    '''
    A graph that extends NetworkX Graph with more analytic parameters and other things.
    '''

    debug = False
    input_debug_links = 100000
    output_debug_nodes = 10
    
    max_links_input = 10 ** 8
    max_nodes_analysis = 10 ** 8     
    
    cached_diameter = None
    cache_internal_growth = {}
    cache_path_lens = {} # keys are nodes, values are tuples maximum and average

    __weight_one = {}          # means "unvisited"
    __weight_two = {True:True} # means "visited" 


    def __init__(self):
        '''
        Constructor
        '''
        super(Graph, self).__init__()
    
        self.__params = {}
        
        self.cores = None
    
        
    def load_edgelist(self, fileobj, num=False, use_big_alphabet=False):
        c = 0
        
        modulo = self.input_debug_links
        total = self.max_links_input
        estimator = TimeEstimator(total/modulo)
        
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
                sys.stdout.write('INFO: INPUT load_edgelist(), link count = %d  %s\n' % (c,time.ctime()))
            if self.debug and c%modulo == 0:
                print 'INFO: %d edges loaded in load_edgelist(), estimated total %d' % (c, total)
                estimator.tick()
                print estimator.log_line()
            if c >= self.max_links_input:
                break

        if self.debug:
            sys.stdout.write('INFO: FINISH INPUT load_edgelist(), link count = %d\n' % c)

    
    def load_only_symmetric_edgelist(self, fileobj):
        '''
        Load from a set of directed links, only bidirectional links are added.
        '''

        sep = None
        
        graph = {}
        count = 0
        for line in fileobj:
            
            if self.debug and count % self.input_debug_links == 0:
                sys.stdout.write('INFO: INPUT load_only_symmetric_edgelist(), link count = %d\n' % count)
                
            if count >= self.max_links_input:
                break
            
            count += 1
            
            if len(line.strip()) == 0:
                continue
            
            s = line.split(sep)
            n1, n2 = s[0], s[1].strip()
            
            if not n1 in graph:
                graph[n1] = []
        
            graph[n1].append(n2)

        if self.debug:
            sys.stdout.write('INFO: FINISH INPUT load_only_symmetric_edgelist(), link count = %d\n' % count)
            sys.stdout.write('INFO: begin second stage\n')
        
        count = 0
        for n1 in graph:
            if self.debug and count % self.output_debug_nodes == 0:
                sys.stdout.write('INFO: INPUT load_only_symmetric_edgelist(), node count = %d\n' % count)
            count += 1
            for n2 in graph[n1]:
                if n2 in graph and n1 in graph[n2]:
                    self.add_edge(n1, n2)
                    graph[n2].remove(n1)

        if self.debug:
            sys.stdout.write('INFO: FINISH INPUT load_only_symmetric_edgelist(), node count = %d\n' % count)

    
    def degrees_iter(self, nodes=None):
        return self.generic_networkx_parameter_iter(nx.degree, 'degrees', None, nodes)

    
    def save_edgelist(self, path, comments='#', delimiter=' ', data=False):
        '''
        Save graph as a set of directed links with format:
        <nodeA> <nodeB>

        G : graph
        
            A NetworkX graph
        
        path : file or string
        
            File or filename to write. Filenames ending in .gz or .bz2 will be compressed.
        
        comments : string, optional
        
            The character used to indicate the start of a comment
        
        delimiter : string, optional
        
            The string uses to separate values. The default is whitespace.
        
        data : bool, optional
        
            If True write a string representation of the edge data.

        Save graph as a set of directed links with format:
        <nodeA> <nodeB>
        <nodeF> <nodeU>
        ...
        etc.        
        '''
        try:
            out = open(path, 'w')
        except:
            out = path
        modulo = 100000
        total = self.number_of_edges()
        estimator = TimeEstimator(total/modulo)
        count = 1        
        for src, dst in self.edges_iter():
            out.write('%s %s\n' % (str(src),str(dst)) )
            if self.debug and count%modulo == 0:
                print 'INFO: %d edges dumped in save_edgelist(), total %d' % (count, total)
                estimator.tick()
                print estimator.log_line()
            count += 1
        #out.close()
        #nx.write_edgelist(self, path, comments, delimiter)
            

    def degrees(self, nodes=None):
        return self.generic_networkx_parameter(nx.degree, 'degrees', None, nodes)

    
    def clustering_indices_iter(self, nodes=None):        
        return self.generic_networkx_parameter_iter(nx.clustering, 'clustering_indices', None, nodes)

    
    def clustering_indices(self, nodes=None):        
        return self.generic_networkx_parameter(nx.clustering, 'clustering_indices', None, nodes)

    
    def average_neighbor_degrees_iter(self, nodes=None):        
        return self.generic_networkx_parameter_iter(self.__average_neighbor_degrees_func, 'average_neighbor_degrees', None, nodes)

    
    def average_neighbor_degrees(self, nodes=None):        
        return self.generic_networkx_parameter(self.__average_neighbor_degrees_func, 'average_neighbor_degrees', None, nodes)

    
    def eccentricities_iter(self, nodes=None):
        return self.generic_networkx_parameter_iter(self.__eccentricity_func, 'eccentricities', None, nodes)

    
    def eccentricities(self, nodes=None):
        return self.generic_networkx_parameter(self.__eccentricity_func, 'eccentricities', None, nodes)

    
    def average_path_lengths_iter(self, nodes=None):
        return self.generic_networkx_parameter_iter(self.__average_path_length_func, 'average_path_lengths', None, nodes)

    
    def average_path_lengths(self, nodes=None):
        return self.generic_networkx_parameter(self.__average_path_length_func, 'average_path_lengths', None, nodes)
    
    
    def max_internal_scaling_iter(self, nodes=None):
        return self.generic_networkx_parameter_iter(self.__max_internal_scaling_func, 'max_internal_scaling_iter', None, nodes)

    
    def max_internal_scaling(self, nodes=None):
        return self.generic_networkx_parameter(self.__max_internal_scaling_func, 'max_internal_scaling', None, nodes)
    
    
    def max_connectivity_iter(self, nodes=None):
        return self.generic_networkx_parameter_iter(self.__max_connectivity_func, 'max_connectivity_iter', None, nodes)

    
    def max_connectivity(self, nodes=None):
        return self.generic_networkx_parameter(self.__max_connectivity_func, 'max_connectivity', None, nodes)
    
    
    def internal_scaling_iter(self, nodes=None):
        return self.generic_networkx_parameter_iter(self.__internal_scaling_func, 'internal_scaling_iter', None, nodes)

    
    def internal_scaling(self, nodes=None):
        return self.generic_networkx_parameter(self.__internal_scaling_func, 'internal_scaling', None, nodes)
    
    
    def connectivity_iter(self, nodes=None):
        return self.generic_networkx_parameter_iter(self.__connectivity_func, 'connectivity_iter', None, nodes)

    
    def connectivity(self, nodes=None):
        return self.generic_networkx_parameter(self.__connectivity_func, 'connectivity', None, nodes)
    
    
    def kcoreness_iter(self, nodes=None):
        if not self.cores:        
            self.cores = nx.find_cores(self)
        return self.generic_networkx_parameter_iter(self.__kcoreness_func, 'kcoreness', self.cores, nodes)


    def kcoreness(self, nodes=None):        
        cores = nx.find_cores(self)
        return self.generic_networkx_parameter(self.__kcoreness_func, 'kcoreness', cores, nodes)

    
    def triangles_iter(self, nodes=None):        
        return self.generic_networkx_parameter_iter(self.__triangles, 'triangles', None, nodes)

    
    def triangles(self, nodes=None):        
        return self.generic_networkx_parameter(self.__triangles, 'triangles', None, nodes)

    
    def generic_networkx_parameter_iter(self, nx_func, name, pre_dic=None, nodes=None):
            
        c = 0
        for node in nodes or self.nodes_iter():
            
            if pre_dic:
                val = nx_func(self, node, pre_dic)
            else:
                val = nx_func(self, node)
                
            yield val

            c += 1
            #if self.debug and c % self.output_debug_nodes == 0:
            #    sys.stdout.write('INFO: OUTPUT %s(), node count = %d\n' % (name, c))
            if c >= self.max_nodes_analysis:
                break
            
        if self.debug and c % self.output_debug_nodes == 0:
            sys.stdout.write('INFO: FINISH OUTPUT %s(), node count = %d\n' % (name, c))
        

    def generic_networkx_parameter(self, nx_func, name, pre_dic=None, nodes=None):
            
        ret_value = []            
            
        c = 0
        for node in nodes or self.nodes_iter():
            
            if pre_dic:
                val = nx_func(self, node, pre_dic)
            else:
                val = nx_func(self, node)
                
            ret_value.append(val)
            
            c += 1
            if self.debug and c % self.output_debug_nodes == 0:
                sys.stdout.write('INFO: OUTPUT %s(), node count = %d\n' % (name, c))
            if c >= self.max_nodes_analysis:
                break
            
        if self.debug and c % self.output_debug_nodes == 0:
            sys.stdout.write('INFO: FINISH OUTPUT %s(), node count = %d\n' % (name, c))

        return ret_value
        

    def __eccentricity_func(self, G, node):
                
        if not node in self.cache_path_lens:
            

            self.__update_path_lens_cache(G, node)

        elif self.debug:
            
                print 'INFO: using cached path lens for node %s ' % str(node)
            
        return self.cache_path_lens[node][0]        


    def __update_path_lens_cache(self, G, node):
            
        spaths = nx.single_source_shortest_path_length(G, node)
        
        path_max, path_len = 0, 0
        for _,l in spaths.iteritems():
            if l > path_max:
                path_max = l
            path_len += l
        self.cache_path_lens[node] = path_max, float(path_len)/len(spaths)


    def __average_path_length_func(self, G, node):
        
        if not node in self.cache_path_lens:

            self.__update_path_lens_cache(G, node)

        elif self.debug:
            
                print 'INFO: using cached path lens for node %s ' % str(node)
            
        return self.cache_path_lens[node][1]        


    def average_neighbor_degree(self, node):
        return self.__average_neighbor_degrees_func(self, node)


    def __average_neighbor_degrees_func(self, G, node):
        neighbors = G.neighbors(node)
        if len(neighbors) == 0:
            return 0.0
        else:
            return float (sum (self.degrees_iter(neighbors))) / len(neighbors)


    def __max_internal_scaling_func(self, G, node):        
        return max( G.internal_scaling_dimension(node) )


    def __max_connectivity_func(self, G, node):        
        return max( G.connectivity_dimension(node) )


    def __internal_scaling_func(self, G, node):        
        return G.internal_scaling_dimension(node) 


    def __connectivity_func(self, G, node):        
        return G.connectivity_dimension(node)


    def __kcoreness_func(self, G, node, pre_dic):
        return pre_dic[node]


    def __triangles(self, big_graph, node):
        
        #if 'triangles' in self.__params and len(self.__params['triangles']) == self.number_of_nodes():
        #    return self.__params['triangles'][node]
        
        deg = self.degree(node)
        clust = nx.clustering(big_graph, node)
        return int( clust * deg * (deg-1) / 2 ) 
            
            
    def show(self, mode=None):
        
        if not mode:
            nx.draw(self)
        elif mode == 'random':
            nx.draw_random(self)
        elif mode == 'circular':
            nx.draw_circular(self)
        elif mode == 'spectral':
            nx.draw_spectral(self)
        
        plt.show()


    def random_edges(self, k=1, data=False):
        """Choose k random edges uniformly from graph.
    
        For undirected graphs this might produce duplicates
        since each edge is considered twice, once for each
        representation u-v and v-u.  Duplicates can be removed by
        using set(random_edges()).
        
        Extracted from Eric Hagberg post:
        http://groups.google.com/group/networkx-discuss/browse_thread/thread/a87dd6ca7063a778?pli=1
        """
        return random_items(self.edges(data=data), k=k) 

          
    def random_nodes(self, k=1):
        """Choose k random nodes uniformly from graph.
        """
        ret = []
        use_random = True
        for node, _ in self.get_parameter_cache_iter('degree', random=use_random):
            ret.append( node )
        return ret
        #return random_items(self.nodes_iter(), k=k) 
          

    def lookahead_edges(self, nbunch, lookahead):

        nbunch = [n for n in nbunch if n in self.nodes()]        
        edge_bunch_list = [self.edges(nbunch)]
        
        for _ in range(lookahead - 1):
            new_nodes = [d for _, d in edge_bunch_list[-1]]
            edge_bunch_list.append(self.edges(new_nodes))
            
        ret = set([])
        for edge_set in edge_bunch_list:
            ret = ret.union(edge_set)
        return ret


    def diameter(self):
        if self.debug:
            print 'INFO: computing graph diameter...'
        dia = nx.diameter(self)
        if self.debug:
            print 'INFO: done computing graph diameter.'
        return dia
    

    def internal_scaling_dimension_iter(self, node, diameter=100):

        return self.__dimension_iter(node, self.internal_scaling_growth_iter, diameter)

    
    def internal_scaling_dimension(self, node, diameter=100):

        return self.__dimension(node, self.internal_scaling_growth, diameter)

    
    def __dimension_iter(self, node, growth_func, diameter=None):

        if not diameter:
            if not self.cached_diameter:
                self.cached_diameter = self.diameter()
            diameter = self.cached_diameter

        growth = growth_func( node, diameter ) 
        for g, l in izip(growth,range(diameter)):
            if g == 0 or l <= 1:
                yield -1.0 
            else:
                yield log(g)/log(l) 
    
    
    def __dimension(self, node, growth_func, diameter=None):

        if not diameter:
            if not self.cached_diameter:
                self.cached_diameter = self.diameter()
            diameter = self.cached_diameter

        growth = growth_func( node, diameter )
        ret = [] 
        for g, l in izip(growth,range(diameter)):
            if g == 0 or l <= 1:
                ret.append( -1.0 ) 
            else:
                ret.append( log(g)/log(l) )
        return ret 
    
    
    def internal_scaling_growth_iter(self, node, diameter=None):

        nodes = set([node])
        visited_nodes = set([])        
        yield 1    

        if not diameter:
            if not self.cached_diameter:
                self.cached_diameter = self.diameter()
            diameter = self.cached_diameter

        prev = None
        if diameter:
            diameter -= 1        
        for _ in range( diameter ):

            new_edges = self.edges(nodes)
            visited_nodes.union( nodes )

            new_nodes = set([])
            for v, w in new_edges:
                if not w in visited_nodes:
                    new_nodes.add( w )
                if not v in visited_nodes:
                    new_nodes.add( v )

            if not prev:
                prev = len(visited_nodes) + len(new_nodes) 
            elif prev == len(visited_nodes) + len(new_nodes):
                break
            else:
                prev = len(visited_nodes) + len(new_nodes) 
        
            if self.debug:
                #print 'internal scaling growth (iter) : %d' % (len(visited_nodes) + len(new_nodes) )
                pass 
                
            yield len(visited_nodes) + len(new_nodes) 
            nodes = new_nodes
            
        
    def internal_scaling_growth(self, node, diameter=None):

        nodes = set([node])
        visited_nodes = set([])
        
        ret = []
        ret.append( 1 )        

        if not diameter:
            if not self.cached_diameter:
                self.cached_diameter = self.diameter()
            diameter = self.cached_diameter

        if (node,diameter) in self.cache_internal_growth:
            if self.debug:
                print 'INFO: using cached internal_growth'
            return self.cache_internal_growth[(node,diameter)]

        prev = None
        for _ in range( diameter - 1  ):

            new_edges = self.edges(nodes)
            visited_nodes.union( nodes )

            new_nodes = set([])
            for v, w in new_edges:
                if not w in visited_nodes:
                    new_nodes.add( w )
                if not v in visited_nodes:
                    new_nodes.add( v )

            if not prev:
                prev = len(visited_nodes) + len(new_nodes) 
            elif prev == len(visited_nodes) + len(new_nodes):
                break
            else:
                prev = len(visited_nodes) + len(new_nodes) 
        
            if self.debug:
                #print 'internal scaling growth : %d' % (len(visited_nodes) + len(new_nodes) )
                pass 
                
            ret.append( len(visited_nodes) + len(new_nodes) ) 
            nodes = new_nodes
        
        if self.debug:
            print 'INFO: caching internal growth for node %s and diameter %d' % (str(node),diameter)
        self.cache_internal_growth[(node,diameter)] = ret    
        return ret
            
        
    def connectivity_dimension_iter(self, node, diameter=100):
        
        return self.__dimension_iter(node, self.connectivity_growth_iter, diameter)
    
        
    def connectivity_dimension(self, node, diameter=100):
        
        return self.__dimension(node, self.connectivity_growth, diameter)
    
        
    def connectivity_growth_iter(self, node, diameter=None):

        internal_growth = self.internal_scaling_growth_iter(node, diameter)
        
        prev = None
        for i in internal_growth:
            if not prev:
                prev = i
            else:
                yield i - prev
        yield 0 
                

    def connectivity_growth(self, node, diameter=None):

        internal_growth = self.internal_scaling_growth(node, diameter)
        
        prev = None
        ret = []
        for i in internal_growth:
            if not prev:
                prev = i
            else:
                ret.append( i - prev )
        ret.append( 0 )
        return ret 
                

    def compressed_by_degree_graph(self, use_big_alphabet=True):
    
        orig_max_nodes_analysis = self.max_nodes_analysis        
        self.max_nodes_analysis = self.number_of_nodes()
    
        encoding = zip(self.nodes_iter(), self.degrees_iter())
        encoding.sort( lambda x, y: cmp(x[1],y[1]) )
        encoding.reverse()
        
        if use_big_alphabet:
            base = Base()
            base_enc = base.num2base
        else:
            base_enc = identity
            
        encoding = dict( zip( [t[0] for t in encoding], range(len(encoding)) ) )
        
        new_graph = Graph()
        if self.debug:
            print 'encoding nodes...'
        for node in self.nodes_iter():            
            new_graph.add_node( base_enc( encoding[node] ) )
        
        if self.debug:    
            print 'encoding edges...'            
        for v, w in self.edges_iter():            
            new_graph.add_edge( base_enc( encoding[v] ), base_enc( encoding[w] ), )

        self.max_nodes_analysis = orig_max_nodes_analysis
        return new_graph
    
    
    def save_compressed_graph(self, outfile, use_big_alphabet=True):
        
        g2 = self.compressed_by_degree_graph(use_big_alphabet)
        output = StringIO()
        g2.save_edgelist(output)
        
        cont = output.getvalue()
        output.close()
        comp_cont = zlib.compress( cont, 9 ) 

        enc_comp_cont = base64.b64encode( comp_cont )

        if outfile == str(outfile):
            outfile = open(outfile,'w')

        outfile.write( "compressed_graph = '''\n%s\n'''" % enc_comp_cont )

          
    def load_compressed_graph(self, module, use_big_alphabet=True, has_num=True):
        
        enc_comp_cont = module.compressed_graph.strip()

        comp_cont = base64.b64decode( enc_comp_cont )

        cont = zlib.decompress(comp_cont) 

        self.load_edgelist(StringIO(cont), has_num, use_big_alphabet)


    def bigger_component(self):
        
        #if nx.is_connected(self):
        #    return self
        
        graph = Graph()
        graph.add_edges_from(nx.connected_component_subgraphs(self)[0].edges_iter())
        
        return graph


    def add_bigger_component_to(self, graph):
        
        #if nx.is_connected(self):
        #    return self

        print 'nx.connected_components(self) ...'
        nx.connected_components(self)

        graph.add_edges_from(self.edges_iter(nx.connected_components(self)[0]))
       
        return graph


    def connected_components(self):
        return nx.connected_components(self)


    def save_bigger_component(self, filename):

        graph = self.bigger_component()
        graph.save_edgelist(filename)
        

    # Indexed parameters methods.

    def check_parameter_name(self, parameter_name):

        # check that the parameter name is ok
        findings = re.findall('[a-z_]+[a-z_0-9]*', parameter_name)
        if len(findings)==0 or len(findings[0]) != len(parameter_name):
            raise GraphException('Error: bad parameter name, only [a-z_]+ allowed!') 
        
    
    def add_parameter_cache(self, parameter_name):

        self.check_parameter_name(parameter_name)

        if not parameter_name in self.__params:
            self.__params[parameter_name] = IndexedTable()
    
    
    def has_parameter_cache(self, parameter_name):
        
        return parameter_name in self.__params
    
    
    def remove_parameter_cache(self, parameter_name):

        self.check_parameter_name(parameter_name)
                
        del self.__params[parameter_name]
        
    
    def index_parameter_cache(self, parameter_name):

        self.check_parameter_name(parameter_name)
        
        pass
    
    
    def remove_index_parameter_cache(self, parameter_name):

        self.check_parameter_name(parameter_name)
        
        pass

    def check_float(self, value):
        
        try:
            return float(value)
        except:
            raise GraphException('Error: value %s is not a floating-point or equivalent number!' % str(value))
        
    
    def insert_parameter_cache(self, param_name, node, value):
        
        value = self.check_float(value)

        self.__params[param_name][node] = value
    

    def update_parameter_cache(self, param_name, node, value):
        '''
        
        '''
        
        #self.check_parameter_name(param_name)
        #self.check_node(node)
        value = self.check_float(value)

        if not self.has_node(node):
            raise GraphException('Error: node %s not in BigGraph instance!' % str(node) )
    
        self.__params[param_name][node] = value

    
    def dec_parameter_cache(self, param_name, node):

        old_val = self.__params[param_name][node]
        self.__params[param_name][node] = (old_val - 1 > 0) and (old_val - 1) or 0 

    
    def inc_parameter_cache(self, param_name, node):
        
        old_val = self.__params[param_name][node]
        self.__params[param_name][node] = old_val + 1 

    
    def get_parameter_cache(self, param_name, node):

        if node in self.__params[param_name]:
            return self.__params[param_name][node]
        else:
            return None
        
    
    def get_max_value_parameter_cache(self, param_name):

        raise GraphException('Not implemmented!')
        
    
    def get_sum_value_parameter_cache(self, param_name):
        
        print 'summing table ...'
        ret = 0
        indexed_table = self.__params[param_name]
        for item in indexed_table.items():
            #print 'item', item
            #print 'indexed_table.preimage_size(item)', indexed_table.preimage_size(item)
            ret += indexed_table.preimage_size(item) * item
        #print 'unseen_triangles', ret / 3
        #print 'total_triangles', self.total_triangles()
        #print '-'*50
        print 'end summing table ...'
        return ret          
    
    
    def get_parameter_cache_inverse(self, param_name, value):

        for node in self.__params[param_name].preimage(value):
            yield node
        
    
    def get_parameter_cache_inverse_between(self, param_name, lower, upper):
        
        raise GraphException('Not implemmented!')
        
    
    def get_parameter_cache_inverse_count(self, param_name, value):

        return self.__params[param_name].preimage_size(value)
        
    
    def get_parameter_cache_iter(self, param_name, random=False, ascending=False):    

        self.check_parameter_name(param_name)

        for node, value in self.__params[param_name].iterate(random, ascending):
            yield node, value

    def create_indices(self):
        pass
    
    
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
        
        self.index_parameter_generic('shell', self.kcoreness_iter)
        
        
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
        
        try:
            del self.__params[param_name]
        except:
            pass

        self.add_parameter_cache(param_name)
        self.__params[param_name] = copy.deepcopy( self.__params['degree'] )
        
              
    def index_parameter_from_parameter(self, param_src, param_dst, ):
        
        try:
            del self.__params[param_dst]
        except:
            pass

        self.add_parameter_cache(param_dst)
        self.__params[param_dst] = copy.deepcopy( self.__params[param_src] )
        
        
    def index_all_parameters(self):

        self.create_index_degree()
        if self.debug:
            print 'done'
            print 'creating knn index ...'
        self.create_index_knn()
        if self.debug:
            print 'done'
            print 'creating clustering index ...'
        self.create_index_clustering()
        if self.debug:
            print 'done'
            print 'creating kcores index ...'
        self.create_index_kcores()
        if self.debug:
            print 'done'
            print 'creating unseen degree index ...'
        self.create_index_unseen_degree()

        
    def load_index_and_pickle(self, fileobj, num=False, outfilename=None):
        
        if self.debug:
            print 'loading graph ...'
        self.load_edgelist(fileobj, num)
        
        self.create_indices()
        
        if self.debug:
            print 'done'
            print 'creating degree index ...'
        self.create_index_degree()
        if self.debug:
            print 'done'
        
        if self.debug:
            print 'dumping Graph pickle ...'
        self.pickle_dump(outfilename)
        if self.debug:
            print 'done.'
        

    def pickle_dump(self, outfilename):

        if str(outfilename) == outfilename:
            output = open(outfilename, 'wb')
        else:
            output = outfilename
            
        cPickle.dump(self, output, -1)


    # methods related to edge weight

    def update_edge_weight(self, src, dst, weight):

        if weight == 1:
            self[src][dst] = self.__weight_one
            self[dst][src] = self.__weight_one
        elif weight == 2:
            self[src][dst] = self.__weight_two
            self[dst][src] = self.__weight_two
        else:
            raise GraphException('One weights 1 or 2 supported for edges!')
    
    
    def edge_weight(self, node1, node2):

        if self[node1][node2] == self.__weight_one:
            return 1
        elif self[node1][node2] == self.__weight_two:
            return 2            
        else:
            raise GraphException('One weights 1 or 2 supported for edges!')
    
    
    def reset_edge_weights(self):
        
        for src, dst in self.edges_iter():
            self[src][dst] = self.__weight_one


    def total_triangles(self):

        if self.has_parameter_cache('triangles'):
            return self.get_sum_value_parameter_cache('triangles') / 3.0
        else:
            raise GraphException('triangles not indexed!')

#        ret = 0
#        for n1, n2 in self.edges_iter():
#            for n3 in self.neighbors_iter(n2):
#                for n4 in self.neighbors_iter(n3):
#                    if n4 == n1:
#                        ret += 1
#        
#        return ret / 3
        
    
    def total_unseen_triangles(self):

        if self.has_parameter_cache('unseen_triangles'):
            return self.get_sum_value_parameter_cache('unseen_triangles') / 3.0
        else:
            raise GraphException('unseen_triangles not indexed!')
        
        
    def total_seen_triangles(self):

        if self.has_parameter_cache('seen_triangles'):
            return self.get_sum_value_parameter_cache('seen_triangles') / 3.0
        else:
            raise GraphException('unseen_triangles not indexed!')
        
        
    def total_triangles_weight(self, weight=1):
        
        if weight==1:
            weight = self.__weight_one
        elif weight==2:
            weight = self.__weight_two
        else:
            raise GraphException('One weights 1 or 2 supported for edges!')
        
        ret = 0
        for n1, n2 in self.edges_iter():
            if self[n1][n2] == weight:
                for n3 in self.neighbors_iter(n2):
                    if self[n2][n3] == weight:
                        for n4 in self.neighbors_iter(n3):
                            if self[n3][n4] == weight:
                                if n4 == n1:
                                    ret += 1

        return ret / 3
        
        
    def triangles_weight(self, node, weight=1):
        
        if weight==1:
            weight = self.__weight_one
        elif weight==2:
            weight = self.__weight_two
        else:
            raise GraphException('One weights 1 or 2 supported for edges!')
        
        if not node in self:
            return 0
        
        ret = 0
        n1 = node
        for n2 in self.neighbors_iter(n1):
            if self[n1][n2] == weight:
                for n3 in self.neighbors_iter(n2):
                    if self[n2][n3] == weight:
                        for n4 in self.neighbors_iter(n3):
                            if self[n3][n4] == weight:
                                if n4 == n1:
                                    ret += 1

        return ret / 2
    
    
    def add_random_component(self, graph):
        
        queue = set([self.random_nodes()[0]])
        visited = set([])
        while len(queue) > 0:
        
            node = queue.pop()
            visited.add( node )
            
            for neigh in self.neighbors_iter(node):
                
                if not neigh in visited:

                    queue.add( neigh )
        
                if not graph.has_edge(node, neigh):
                    graph.add_edge(node, neigh)
        
        return graph
    
          
    def save_snowball_edgelist(self, filename):
        
        out = open(filename, 'w')

        modulo = 10000
        total = self.number_of_edges()
        estimator = TimeEstimator(total/modulo)
        count = 0

        queue = [self.random_nodes()[0]]
        visited = set([])
        while len(queue) > 0:
        
            # impl: node = queue.pop()
            node = queue[0]
            queue = queue[1:]
            
            visited.add( node )
            
            for neigh in self.neighbors_iter(node):
                
                if not neigh in visited:

                    queue.append( neigh )
        
                    out.write('%s %s\n' % (str(node),str(neigh)))
                    count += 1

                    if self.debug and count%modulo == 0:
                        print 'INFO: %d edges dumped in save_snowball_edgelist(), total %d' % (count, total)
                        estimator.tick()
                        print estimator.log_line()
                        
            out.flush()


if __name__ == '__main__':
    
    graph = Graph()
    graph.run_tests()
    


