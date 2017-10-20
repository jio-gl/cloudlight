'''
Created on Sep 11, 2010

@author: jose
'''

from cloudlight.classes.graph import Graph
    
    
# Builder
    
class Product(object):

    def __init__(self, initial=None):

        self.result = initial


    def add(self, elem, *args):
        self.elem = elem
        className = elem.__class__.__name__
        meth = getattr(self.product, 'add' + className, self.add_default)
        return meth(elem, *args)

    
    
class Builder(object):

    def __init__(self):
        self.product = None
        self.initial = None
 
    def create_new_product(self):
        self.product = self.initial

    def add(self, elem, *args):
        self.elem = elem
        className = elem.__class__.__name__
        meth = getattr(self, 'add' + className, self.add_default)
        return meth(elem, *args)

    def add_default(self, elem, *args):
        raise Exception('attribute add%s not implemmented!' % elem.__class__.__name__)


class NullBuilder(Builder):

    def __init__(self):
        super(NullBuilder,self).__init__()
        
    def add_default(self, elem, *args):
        return


class GraphBuilder(Builder):

    def __init__(self):
        super(GraphBuilder,self).__init__()
        self.initial = Graph()
        
    def addNode(self, elem):
        self.product.add_node(elem)
 
    def addtuple(self, elem):
        self.product.add_edge(elem[0], elem[1])

    def addGraph(self, elem):
        for node in elem.nodes_iter():
            self.product.add_node(node)
        for src, dst in elem.edges_iter():
            self.product.add_edge(src, dst)
    

class SumBuilder(Builder):

    def __init__(self):
        super(SumBuilder,self).__init__()
        self.initial = 0.0
        
    def addint(self, elem):
        self.product += elem
 
    def addfloat(self, elem):
        self.product += elem

 
class StringBuilder(Builder):

    def __init__(self):
        super(StringBuilder,self).__init__()
        self.initial = ''
        
    def addstr(self, elem):
        self.product += elem
