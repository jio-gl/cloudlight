#!/usr/bin/python
'''
Created on Apr 27, 2010

@author: jose
'''

import sys

from cloudlight import Plot


class PrivacyAttackResult:
    
    def __init__(self, lookahead, coverage, coverage_type, strategy, effort, date):
        
        self.lookahead = lookahead
        self.coverage  = coverage
	self.coverage_type = coverage_type
        self.strategy  = strategy
        self.effort    = effort
        self.date      = date


class PrivacyResultsPlotter:
    
    
    def __init__(self):
            
        self.plotter = Plot()
        

    def load_all_results(self):
        
        filename =  len(sys.argv) > 1 and sys.argv[1] or None 
    
        if not filename:
            print 'Error: first argument missing, input filename with space separated graph!'
            exit(-1)
            
        folder =  len(sys.argv) > 2 and sys.argv[2] or None 
    
        if not folder:
            print 'Error: second argument missing, output folder name!'
            exit(-1)
            
        coverage =  len(sys.argv) > 3 and sys.argv[3] or None 
    
        if not coverage:
            print 'Error: second argument missing, coverage type !'
            exit(-1)

        if coverage == 'link':
                self.plotter.y_label = 'Link coverage'
		self.coverage_type = 'link_coverage'
        elif coverage == 'node':
                self.plotter.y_label = 'Node coverage'
		self.coverage_type = 'node_coverage'
        elif coverage == 'triangle':
                self.plotter.y_label = 'Triangle coverage'
		self.coverage_type = 'triangle_coverage'
        elif coverage == 'korolova':
                self.plotter.y_label = 'Complete node coverage'
		self.coverage_type = 'complete_node_coverage'
        else:
                self.plotter.y_label = 'Korolova (complete) node coverage'
            
        data = {}
        
        results = []
        
        lookaheads = set([])
        strategies = set([])
        
        for line in open(filename):
            
            if len(line.strip()) == 0 or line.strip()[0] == '#':
                continue
            
            line_s    = line.split()
            
            lookahead = int(line_s[0])
            lookaheads.add( lookahead )
            coverage  = float(line_s[1])
            coverage_type  = line_s[2]
            strategy  = line_s[3]
            strategies.add( strategy )
            effort    = int(line_s[4])
            date      = line_s[5]
            
            result = PrivacyAttackResult(lookahead, coverage, coverage_type, strategy, effort, date)
            
            results.append( result )
    
        self.results = results
        self.lookaheads = lookaheads
        self.strategies = strategies
        self.filename = filename
        self.folder = folder
    
    
    def plot_per_lookahead(self, log_x=False):
        
        for lookahead in self.lookaheads: #self.lookaheads:
            
            self.plotter.clear()
            self.plotter.title = 'Lookahead = %d | nodes = %d edges = %d' % (lookahead,self.nodes,self.edges)
            self.plotter.x_label = 'effort (fraction of nodes bribed)' 
        
            ps, ps_leg = [], []

            for strategy in self.strategies:

                if not strategy in self.strat_exceptions: 
                
                    x, y = [], []
                    
                    for result in self.results:
                        
                        if result.lookahead == lookahead and result.strategy == strategy and result.coverage < 1.0 and result.coverage_type == self.coverage_type:
                                
                                y.append( result.coverage )
                                x.append( float(result.effort) / self.nodes )
    
                    
                    p = self.plotter.plot(x, y, log_x,  False,  True, False)
                    ps.append( p ) 
                    ps_leg.append( "strat=%s" % strategy.replace('start_','')  )
                
            self.plotter.legend(ps, ps_leg)
            if not log_x:
                self.plotter.save(self.folder + '/lookahead-%d-%s.png' % (lookahead,self.coverage_type))
                self.plotter.save(self.folder + '/lookahead-%d-%s.eps' % (lookahead,self.coverage_type))
            else:
                self.plotter.save(self.folder + '/lookahead-%d-%s-log.png' % (lookahead,self.coverage_type))
                self.plotter.save(self.folder + '/lookahead-%d-%s-log.eps' % (lookahead,self.coverage_type))
            

    def plot_per_strategy(self, log_x=True):

        for strategy in self.strategies:

            if not strategy in self.strat_exceptions: 
        
                self.plotter.clear()
                self.plotter.title = 'Strategy = %s | nodes = %d edges = %d' % (strategy,self.nodes,self.edges)
                self.plotter.x_label = 'effort (fraction of nodes bribed)' 
            
                ps, ps_leg = [], []
            
                for lookahead in self.lookaheads: #self.lookaheads:
    
                    #if lookahead == 0:
                    #    continue
                    
                    x, y = [], []
                    
                    for result in self.results:
                        
                        if result.lookahead == lookahead and result.strategy == strategy and result.coverage <= 1.0 and result.coverage_type == self.coverage_type:
                            
                                
                                y.append( result.coverage )
                                x.append( float(result.effort) / self.nodes )
    
                    
                    p = self.plotter.plot(x, y,  log_x, False, True, False)
                    ps.append( p ) 
                    ps_leg.append( "lookahead = %d" % lookahead  )
                    
                self.plotter.legend(ps, ps_leg)       
                if not log_x:     
                    self.plotter.save(self.folder + '/strategy-%s-%s.png' % (strategy,self.coverage_type))
                    self.plotter.save(self.folder + '/strategy-%s-%s.eps' % (strategy,self.coverage_type))
                else:
                    self.plotter.save(self.folder + '/strategy-%s-%s-log.png' % (strategy,self.coverage_type))
                    self.plotter.save(self.folder + '/strategy-%s-%s-log.eps' % (strategy,self.coverage_type))
            

if __name__ == '__main__':
    
    
    
    plotter = PrivacyResultsPlotter()
    
    #nodes: 1084938
    #edges: 11717385
    
    #plotter.nodes = 1084938
    #plotter.edges = 11717385

    #plotter.nodes = 79471
    #plotter.edges = 100000

    #plotter.nodes = 148735
    #plotter.edges = 200000

    #plotter.nodes = 281351
    #plotter.edges = 400000

    plotter.nodes = 590000
    plotter.edges = 1000000

    plotter.strat_exceptions = [] #['start_crawlr_seen_triangles', 'start_crawlr_seen_degree']
    #plotter.strat_exceptions = []

    #plotter.nodes = 12578
    #plotter.edges = 90560

    #plotter.nodes = 168826
    #plotter.edges = 1730051
    
    plotter.lookaheads = [0,1,2]
    #plotter.coverage_type = 'node'

    #plotter.edges = 500000
    #plotter.nodes = 310239
    
    plotter.load_all_results()
        
    plotter.plot_per_lookahead()
    
    plotter.plot_per_lookahead(log_x=True)
    
    plotter.plot_per_strategy()
                    
    plotter.plot_per_strategy(log_x=False)
                    
                    
                    
        
        
