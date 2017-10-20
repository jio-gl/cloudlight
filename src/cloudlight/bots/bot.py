'''
Created on Mar 27, 2010

@author: jose
'''

    

from cloudlight.bots.builder import GraphBuilder, NullBuilder
from cloudlight.bots.iterator import GraphIterator
from cloudlight.bots.visitor import IdentityVisitor, GraphPrinterVisitor


class BotException(Exception):
    pass
    

class Bot(object):
    
    def process(self, graph):
    
        self.graph = graph
        
        self.create_new_product()
        
        for elem in self:
            
            self.add( self.visit(elem) ) 
        
        return self.product
        

# Examples

class CollateralBot(GraphIterator, GraphBuilder, Bot): pass # subclass with some Visitor with collateral effects!

class CopyBot(GraphIterator, IdentityVisitor, GraphBuilder, Bot): pass
        
class PrettyPrintBot(GraphIterator, GraphPrinterVisitor, NullBuilder, Bot): pass



if __name__ == '__main__':
    
    pass