'''
Created on Aug 27, 2010

@author: jose
'''


class Visitor(object):
    '''
    http://peak.telecommunity.com/DevCenter/VisitorRevisited
    http://docs.python.org/tutorial/classes.html#multiple-inheritance
    '''

    def visit(self, elem, *args):
        self.elem = elem
        className = elem.__class__.__name__
        meth = getattr(self, 'visit' + className, self.visit_default)
        return meth(elem, *args)

    def visit_default(self, elem, *args):
        return None


class IdentityVisitor(Visitor):

    def visit(self, elem, *args):
        self.elem = elem
        className = elem.__class__.__name__
        meth = getattr(self, 'visit' + className, self.visit_default)
        return meth(elem, *args)

    def visit_default(self, elem, *args):
        return elem
        

class GraphVisitor(Visitor):

    def visitNode(self, node, *args):
        
        print 'Visitando nodo: id = %s' % node.id
        pass 
    

    def visittuple(self, edge, *args):
        
        print 'Visitando arista: src.id = %s  dst.id = %s' % (edge.src, edge.dst) 
        pass



class DegreeVisitor(Visitor):        

    def visitNode(self, node):
        return self.graph.degree(node)

    
class GraphPrinterVisitor(Visitor):        

    def visitNode(self, node):
        print 'Node: %s' % (str(node))

    def visittuple(self, tup):
        print 'Edge: %s -- %s' % (str(tup[0]), str(tup[1]))

    def visit_default(self, elem, *args):
        print 'Node (subclass): %s' % (str(elem))
    


        
if __name__ == '__main__':
    
#    FacebookVisitor().visitFacebookNode(FacebookNode('Tito Perez')) 
#    
#    TwitterVisitor().visitTwitterNode(TwitterNode('starvejobs')) 
#
#    class MyVisitor(FacebookVisitor, TwitterVisitor): pass
#
#    MyVisitor().visitFacebookNode(FacebookNode('Tito Perez')) 
#    
#    MyVisitor().visitTwitterNode(TwitterNode('starvejobs')) 

    
    pass   



