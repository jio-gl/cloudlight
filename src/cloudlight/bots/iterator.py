'''
Created on Aug 30, 2010

@author: jose
'''


class Iterator(object):
    
    def __iter__(self):
        raise Exception('not implemmented!')
    
    
        
class GraphIterator(Iterator):
    
    
    def __iter__(self):
    
        for node in self.graph.nodes_iter():
            yield node

        for src, dst in self.graph.edges_iter():
            yield src, dst
    

class NodeIterator(Iterator):
    
    
    def __iter__(self):
    
        for node in self.graph.nodes_iter():
            yield node

        
class EdgeIterator(Iterator):
    
    
    def __iter__(self):
    
        for src, dst in self.graph.edges_iter():
            yield src, dst

        
class BFSIterator(Iterator):
    
    
    def __init__(self):
                
        super(BFSIterator, self).__init__()
        
        self.seed_node = None
        self.debug     = False
        
    
    def __iter__(self):
    
        if self.debug:
            print 'BFSBot BEGIN'
        
        if self.graph.number_of_nodes() == 0:            
            return
        
        if not self.seed_node:
            for node in self.graph.nodes_iter():
                self.seed_node = node
            if not self.seed_node:
                return 
        
        queue = [self.seed_node]
        visited = set([])
        
        while len( queue ) > 0:
            
            node = queue[0]
            queue = queue[1:]
            
            yield node, True
            visited.add( node )
            
            for neigh, edge_attrs in self.graph[node].iteritems():
        
                yield (node, neigh, edge_attrs), False 
                
                if not neigh in visited:
                    queue.append(neigh)
        
        if self.debug:            
            print 'BFSBot END'
    

        
class DFSIterator(Iterator):
    
    
    def __init__(self):
                
        super(BFSIterator, self).__init__()
        
        self.seed_node = None
        self.debug     = False
        
    
    def __iter__(self):
    
        if self.debug:
            print 'DFSBot BEGIN'
        
        if self.graph.number_of_nodes() == 0:            
            return
        
        if not self.seed_node:
            for node in self.graph.nodes_iter():
                self.seed_node = node
            if not self.seed_node:
                return 
        
        queue = [self.seed_node]
        visited = set([])
        
        while len( queue ) > 0:
            
            node = queue[-1]
            queue = queue[:-1]
            
            yield node, True
            visited.add( node )
            
            for neigh, edge_attrs in self.graph[node].iteritems():
        
                yield (node, neigh, edge_attrs), False 
                
                if not neigh in visited:
                    queue.append(neigh)
        
        if self.debug:            
            print 'DFSBot END'
    



if __name__ == '__main__':
    pass