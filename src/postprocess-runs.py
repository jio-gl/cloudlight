#!/usr/bin/python
'''
Created on Dec 23, 2010

@author: jose
'''

import sys

#from statlib import stats
import scipy.stats as stats
import numpy

folder = sys.argv[1]
outname =  sys.argv[2]
type =  sys.argv[3]
coverage =  sys.argv[4]
runs =  int(sys.argv[5])

results = {}
lookaheads = set([])
type_covs = set([])
strats = set([])

for run in range(runs):
    
    fname = '%s%s-%d.%s.%s' % (folder,outname,run,type,coverage)
    
    for line in open(fname):
        
        s = line.split()
        
        strat = s[3]
        lookahead = int(s[0])
        frac_cov = float(s[1])
        type_cov = s[2]
        effort = int(s[4])
        effort_frac = float(s[5])

        lookaheads.add( lookahead )
        type_covs.add( type_cov )
        strats.add( strat )
        
        if not strat in results:
            results[strat] = {}
        if not lookahead in results[strat]:
            results[strat][lookahead] = {}
        if not type_cov in results[strat][lookahead]:
            results[strat][lookahead][type_cov] = {}
        if not effort_frac in results[strat][lookahead][type_cov]:
            results[strat][lookahead][type_cov][effort_frac] = []
        
        #  esfuerzo corrida1 corrida2 ... corrida20
        results[strat][lookahead][type_cov][effort_frac].append( frac_cov )

for lookahead in lookaheads:
    
    for type_cov in type_covs:
        
        for strat in strats: 

            ofile = '%s%s.%s.%s-post-%d-%s-%s' % (folder,outname,type,coverage,lookahead,strat,type_cov)
            o = open(ofile,'w')
            o.write('# effort_frac run1 run2 .... runN\n' )
            for effort_frac in sorted(results[strat][lookahead][type_cov].keys()):
                covs = map( str, results[strat][lookahead][type_cov][effort_frac] )
                o.write('%f %s\n' % (effort_frac, ' '.join( covs )) )
            o.close()

            ofile = '%s%s.%s.%s-post-stats-%d-%s-%s' % (folder,outname,type,coverage,lookahead,strat,type_cov)
            o = open(ofile,'w')
            o.write('# effort_fract mean stdev median min max quartile1 quartile2 quartile3\n' )
            for effort_frac in sorted(results[strat][lookahead][type_cov].keys()):
                covs = results[strat][lookahead][type_cov][effort_frac]
                mean, stdev, median = numpy.mean(covs), numpy.std(covs), stats.median(covs) #stats.stdev(covs), numpy.median(covs)
                cov_min,cov_max = min(covs), max(covs)
                #quartile1, quartile2, quartile3 = stats.lscoreatpercentile(covs,.25),stats.lscoreatpercentile(covs,.50),stats.lscoreatpercentile(covs,.75)
                quartile1, quartile2, quartile3 = stats.scoreatpercentile(covs,25),stats.scoreatpercentile(covs,50),stats.scoreatpercentile(covs,75)
                #scoreatpercentile
                o.write('%f %f %f %f %f %f %f %f %f\n' % (effort_frac, mean, stdev, median, cov_min, cov_max, quartile1, quartile2, quartile3 ) )
            o.close()

if __name__ == '__main__':
    pass