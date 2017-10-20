'''
Created on Mar 27, 2010

@author: jose
'''



from cloudlight.bots.bot import Bot


class Printer(Bot):


    outfile = None


    def __init__(self, outfile=None, decoratedBot=None):
        
        self.outfile = outfile
        self.decoratedBot = decoratedBot


    # visit node
    def visit_node(self, node, graph):

        if self.outfile:
            self.outfile.write( 'NODE: %s\n' % str(node) )
        else:
            return 'NODE: %s' % str(node)


    # visit edge with attributes.
    def visit_edge(self, link, graph):

        if len(list(link)) == 3:
            pr_attrs = ''.join([str(a) for a in link[2]])
        else:
            pr_attrs = ''

        if self.outfile:
            self.outfile.write( 'EDGE: %s -- %s ATTRS: %s\n' % (str(link[0]),str(link[1]),pr_attrs) )
        else:
            return 'EDGE: %s -- %s ATTRS: %s' % (str(link[0]),str(link[1]),pr_attrs)



