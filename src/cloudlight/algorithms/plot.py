'''
Created on Mar 29, 2010
    
@author: jose
'''
import math, sys, random
    
import os



try:
    import numpy as np
except:
    #print 'Warning: module python-numpy missing, probably some plot features will not work!'
    pass

try:
    from scipy import polyval, polyfit
except:
    #print 'Warning: module python-scipy missing, probably some plot features will not work!'
    pass


try:
    import matplotlib.pyplot as plt
except:
    pass

from cloudlight.utils.itertools_recipes import *

class Plot(object):
    '''
    classdocs
    Check http://matplotlib.sourceforge.net/api/pyplot_api.html
    '''

    
    title   = 'Insert title here = Plot().title'
    x_label = 'Plot().x_label'
    y_label = 'Plot().y_label'

    debug = True

    param_title = {
                   'degree' : 'Distribution of node degrees',
                   'clustering' : 'Distribution of node clustering indices',
                   'knn' : 'Distribution of average neighbor degree (knn)',
                   'kcore' : 'Distribution of k-shells',
                   'nodesphere1' : 'Dist of node neighborhood sizes in nodes lookahead 1',
                   'nodesphere2' : 'Dist of node neighborhood sizes in nodes lookahead 2',
                   'nodesphere3' : 'Dist of node neighborhood sizes in nodes lookahead 3',
                   'linksphere1' : 'Dist of node neighborhood sizes in edges lookahead 1',
                   'linksphere2' : 'Dist of node neighborhood sizes in edges lookahead 2',
                   'linksphere3' : 'Dist of node neighborhood sizes in edges lookahead 3',                   
                   'eccentricity' : 'Distribution of eccentricities' ,
                   'path_len' : 'average path length',
                   'scaling' : 'scaling dimension approximation',
                   'connectivity' : 'connectivity dimension approximation',
                   'triangles' : 'dist. of number of triangles per node',
                   }
    
    param_label = {
                   'degree' : 'node degree',
                   'clustering' : 'node clustering index',
                   'knn' : 'node average neighbor degree',
                   'kcore' : 'node k-shell',
                   'nodesphere1' : 'node neighborhood in nodes lookahead 1',
                   'nodesphere2' : 'node neighborhood in nodes lookahead 2',
                   'nodesphere3' : 'node neighborhood in nodes lookahead 3',
                   'linksphere1' : 'node neighborhood in edges lookahead 1',
                   'linksphere2' : 'node neighborhood in edges lookahead 2',
                   'linksphere3' : 'node neighborhood in edges lookahead 3',                   
                   'eccentricity' : 'node eccentricity' ,
                   'path_len' : 'average path length',
                   'scaling' : 'scaling dimension approximation',
                   'connectivity' : 'connectivity dimension approximation',
                   'triangles' : 'number of triangles per node',
                   }
    
    param_variable = {
                   'degree' : 'd',
                   'clustering' : 'c',
                   'knn' : 'knn',
                   'kcore' : 'shell',
                   'nodesphere1' : 'nla1',
                   'nodesphere2' : 'nla2',
                   'nodesphere3' : 'nla3',
                   'linksphere1' : 'ela1',
                   'linksphere2' : 'ela2',
                   'linksphere3' : 'ela3',                   
                   'eccentricity' : 'ecc' ,
                   'path_len' : 'l',
                   'scaling' : 'dim_s',
                   'connectivity' : 'dim_c',
                   'triangles' : 't',
                   }
    
    param_logx = {
                   'degree' : True,
                   'clustering' : True,
                   'knn' : True,
                   'kcore' : True,
                   'nodesphere1' : True,
                   'nodesphere2' : True,
                   'nodesphere3' : True,
                   'linksphere1' : True,
                   'linksphere2' : True,
                   'linksphere3' : True,                   
                   'eccentricity' : False ,
                   'path_len' : False,
                   'scaling' : False,
                   'connectivity' : False,
                   'triangles' : True,
                   }
    
    
    param_logy = {
                   'degree' : True,
                   'clustering' : True,
                   'knn' : True,
                   'kcore' : True,
                   'nodesphere1' : True,
                   'nodesphere2' : True,
                   'nodesphere3' : True,
                   'linksphere1' : True,
                   'linksphere2' : True,
                   'linksphere3' : True,                   
                   'eccentricity' : True ,
                   'path_len' : True,
                   'scaling' : True,
                   'connectivity' : True,
                   'triangles' : True,
                   }
    
    
    param_log_bins = {
                   'degree' : True,
                   'clustering' : True,
                   'knn' : True,
                   'kcore' : True,
                   'nodesphere1' : True,
                   'nodesphere2' : True,
                   'nodesphere3' : True,
                   'linksphere1' : True,
                   'linksphere2' : True,
                   'linksphere3' : True,                   
                   'eccentricity' : False ,
                   'path_len' : False,
                   'scaling' : False,
                   'connectivity' : False,
                   'triangles' : True,
                   }
    
    
    param_interpolate = {
                   'degree' : True,
                   'clustering' : True,
                   'knn' : True,
                   'kcore' : True,
                   'nodesphere1' : True,
                   'nodesphere2' : True,
                   'nodesphere3' : True,
                   'linksphere1' : True,
                   'linksphere2' : True,
                   'linksphere3' : True,                   
                   'eccentricity' : False ,
                   'path_len' : False,
                   'scaling' : True,
                   'connectivity' : True,
                   'triangles' : True,
                   }
    
    
    
    


    def __init__(self, debug=True, interpolate=True):
        '''
        Constructor
        '''
        try:
            plt.clf()
        except:
            pass
        self.debug = debug
        
        self.interpolate = interpolate

        
    def plot(self, x, y, logx=False, logy=False, lines=True, dots=True, legend=None):
        # with errorbars: clip non-positive values
        axes = plt.subplot(111)
        
        # http://matplotlib.sourceforge.net/api/axes_api.html#matplotlib.axes.Axes.set_xscale
        if logx:
            axes.set_xscale("log", nonposx='mask')
        else:
            axes.set_xscale("linear", nonposx='mask')
            
        if logy:
            axes.set_yscale("log", nonposx='mask')
        else:
            axes.set_yscale("linear", nonposx='mask')
        
        arrayx = np.ndarray(len(x))
        for val, i  in zip(x,range(len(x))):
            arrayx[i] = val
        
        arrayy = np.ndarray(len(y))
        for val, i  in zip(y,range(len(y))):
            arrayy[i] = val
        
        ret_val = None
        if dots:
            ret_val = plt.plot(arrayx, arrayy, '.', label=legend, markersize=2)
        if lines:
            ret_val = plt.plot(arrayx, arrayy, '-', label=legend)
        axes.set_xlabel(self.x_label)
        axes.set_ylabel(self.y_label)
        plt.title(self.title)
        plt.grid(True)
        
        return ret_val
        
    
    def hist(self, x, bins=10, log_bins=True, logx=False, logy=False, histrange=None, normed=True, weights=None, cumulative=False,
             bottom=None, histtype='step', align='mid',
             orientation='vertical', rwidth=None, log=False, **kwargs):
        '''
        http://matplotlib.sourceforge.net/api/pyplot_api.html#matplotlib.pyplot.hist
        '''

        axes = plt.subplot(111)
        
        # http://matplotlib.sourceforge.net/api/axes_api.html#matplotlib.axes.Axes.set_xscale
        if logx:
            x = filter(lambda x : x > 0, x)
            axes.set_xscale("log", nonposx='mask')
        else:
            axes.set_xscale("linear", nonposx='mask')
            
        if logy:
            axes.set_yscale("log", nonposx='mask')
        else:
            axes.set_yscale("linear", nonposx='mask')

        arrayx = np.ndarray(len(x))
        for val, i  in zip(x,range(len(x))):
            arrayx[i] = val

        
        if log_bins:
            x_log_bins = self.log_log_bins(x, bins)
        else:
            x_log_bins = bins
           
        plt.title(self.title)
                    
        return plt.hist(arrayx, x_log_bins, histrange, normed, weights, cumulative, bottom, histtype, align, orientation, rwidth, log)
    
    
    def log_log_bins(self, x, bins=10):
        '''
        x : a python list of numbers.
        
        exp ^ 10 = bins_range
        log( exp ^ 10, 10) = log(bins_range, 10)

        http://matplotlib.sourceforge.net/api/pyplot_api.html#matplotlib.pyplot.loglog
        '''

        x = filter(lambda x : x > 0, x)
        #x = [val > 0 and -1 or val  for val in x] # 
        #x = [val + 1.0  for val in x]

        if len(x) == 0:
            return [1.0]*(bins+1)
            
        orig_min_val = min(x)
        
        x = [val/orig_min_val for val in x]

        min_val = min(x)
        max_val = max(x)
        
        bins_range = max_val - min_val + 1
        
        exp = math.log(bins_range, bins - 1 )
        self.exp = exp
        
        log_r = math.log10(bins_range)/bins;
        r = 10.0**log_r

        return [min_val*(r**i) * orig_min_val for i in range(bins+1) ]
        
        
    def show(self):
        plt.show()


    def clear(self):
        plt.clf()
        
        
    def close(self):
        plt.close()
        
        
    def save(self, fname, dpi=None, facecolor='w', edgecolor='w',
                orientation='portrait', papertype=None, format=None,
                transparent=False):
        '''
        http://matplotlib.sourceforge.net/api/pyplot_api.html#matplotlib.pyplot.savefig
        '''
        plt.savefig(fname)
        
        
    def native_hist(self, sample, bins, log_bins, normed=True):
        
        x = sample

        if log_bins:
            bins_data = self.log_log_bins(x, bins)
        else:
            bins_data = self.get_bins(x, bins)

        # TODO
        y = [0]*(bins)
        non_zeros = 0
        for val in sample:
            for i in range( bins ):
                if val >= bins_data[i] and val < bins_data[i+1]:
                    y[i] += 1
                    non_zeros += 1  
        
        for i, val in zip( range( bins ), y):
            y[i] = y[i] / (bins_data[i+1] - bins_data[i])
        
        if normed:
            y = [float(val)/non_zeros for val in y]
        
        return y, bins_data, None


    def native_hist_2d(self, x, y, bins, log_bins, normed=False):
        
        if log_bins:
            bins_data = self.log_log_bins(x, bins)
        else:
            bins_data = self.get_bins(x, bins)

        # TODO
        y_bis = [0]*(bins)
        y_bis_count = [0]*(bins)
        non_zeros = 0
        for val, val2 in zip(x, y):
            for i in range( bins ):
                if val >= bins_data[i] and val < bins_data[i+1]:
                    y_bis[i] += val2
                    y_bis_count[i] += 1
                    non_zeros += 1  
        
        # average
        for i in range(bins):
            if y_bis_count[i] > 0:
                y_bis[i] /= y_bis_count[i]
        
        # proportional to bin size
#        for i, val in zip( range( bins ), y_bis):
#            y_bis[i] = y_bis[i] / (bins_data[i+1] - bins_data[i])
        
        # a frequency ?
        if normed:
            y_bis = [float(val)/non_zeros for val in y]
        
        return y_bis, bins_data, None


    def get_bins(self, x, bins):
        
        x = filter(lambda x : x > 0, x)

        if len(x) == 0:
            return [1.0]*(bins+1)
            
        orig_min_val = min(x)
        
        x = [val/orig_min_val for val in x]

        min_val = min(x)
        max_val = max(x)
        
        bins_range = max_val - min_val + 1

        return [(min_val + i*bins_range/bins) * orig_min_val for i in range(bins+1)]        


    def histogram_interpolate(self, x):
        new_x = []
        pred = None
        for val in x:
            if not pred:
                pred = val
            else:                
                # another posibility
                #new_x.append( ((math.log(val + pred,self.exp) + math.log(pred,self.exp) ) / 2.0 ) ** self.exp )
                new_x.append( (val + pred) / 2.0  )
                pred = val
                 
        return new_x


    def raw_hist_data(self, sample, normed=True):
        
        hist = {}
        for val in sample:
            if not val in hist:
                hist[val] = 1
            else:
                hist[val] += 1
        
        hist = list(hist.iteritems())
        hist.sort( lambda a,b : cmp(a[0],b[0]) )
        
        if not normed:
            x = [e[0] for e in hist]
            y = [e[1] for e in hist]
        else:
            x = [e[0] for e in hist]
            y = [float(e[1])/len(sample) for e in hist]
        
        return y, x
  
  
    def raw_hist_data_2d(self, x, y, normed=False):
        
        hist = {}
        hist_count = {}        
        for x_i, y_i in zip(x,y):
            if not x_i in hist:
                hist[x_i] = y_i
                hist_count[x_i] = 1
                
            else:
                hist[x_i] += y_i
                hist_count[x_i] += 1
                
        for x_i in hist:            
            hist[x_i] /= float(hist_count[x_i])
        
        hist_deviation = {}
        #for x_i in hist:            
        #    ave = hist[x_i]
        #    sqrs = [(ave-y_j)**2 for x_j,y_j in zip(x,y) if x_j==x_i and y_j >= 0.0] 
        #    sqr_sum = sum(sqrs)
        #    hist_deviation[x_i] = math.sqrt(sqr_sum / len(sqrs))
        
        hist = list(hist.iteritems())
        hist.sort( lambda a,b : cmp(a[0],b[0]) )

        hist_deviation = list(hist_deviation.iteritems())
        hist_deviation.sort( lambda a,b : cmp(a[0],b[0]) )
        
        if not normed:
            x = [e[0] for e in hist]
            y = [e[1] for e in hist]
            y_err = [e[1] for e in hist_deviation]
        else:
            x = [e[0] for e in hist]
            y = [float(e[1])/len(x) for e in hist]
            y_err = [float(e[1])/len(x) for e in hist_deviation]
        
        return y, x, y_err
  
  
    def log_bins2(self, v, bins=30):

        # removing zeros
        total = len(v)
        #v = [val for val in v if val != 0.0]
        #non_zeros = len(v)

        n = bins
        
        d_max = max(v)
        d_min = min(v)

        log_r = math.log10(d_max - d_min + 1)/n;
        r = 10.0**log_r

        # Calculate start for each bin
        points = [0.0] * (n+1)

        points[0] = d_min
        for i in range(1,n):
            points[i] = points[i-1]*r;

        # removing repeated values
        points = sorted(list(set( points[:-1] ))) + [0.0]

        points = [round(p) for p in points]
        npoints = []
        for p, i in zip(points,range(len(points))):
            if len(npoints) == 0 or points[i-1] != p:
                npoints.append( p )
        points = npoints

        # limit of the last bin
        final_bin_num = len(points)
        # includes the last point in the last bin (simulates right-closed)
        points[final_bin_num-1] = d_max + 1

        points_y = [0.0]*(final_bin_num-1)
        points_x = [0.0]*(final_bin_num-1)

        #total=0
        i = 0
        for low in points[:-1]:
            if i < final_bin_num-1 and points[i] <= d_max:
                # left-closed, right-open
                high = points[i+1] - 1

            #calculate the range (low;high)
            points_y[i]= sum(filter( lambda e : e >= low and e < high+1, v)) / (((high+1)-low) * total)            
            points_x[i] = (low + high) / 2

            #total=total+(high-low+1)*points_y(i)
            i = i+1

        print '-'*60
        print points_x
        print '-'*60
        print points_y
         
           
          
        return points_x, points_y

        
    def dist_plot(self, sample, bins=10, log_bins=True, logx=True, logy=True):
        
        #x, y = self.log_bins2(sample, bins)
        y, x, _ = self.native_hist( sample, bins, log_bins)
        x = self.histogram_interpolate(x)
        
        detailed_y, detailed_x = self.raw_hist_data(sample) #self.native_hist( sample, len(set(sample)), False)
    
        
                        
        ps, ps_leg = [], []
        
        p2 = self.plot(detailed_x, detailed_y, logx, logy, False)
        ps.append( p2 ) 
        ps_leg.append( "Complete histogram" )

        p1 = self.plot(x, y, logx, logy, True, True)
        ps.append( p1 ) 
        ps_leg.append( "Hist. log. bin." )

        if self.interpolate:
            linear_y, linear_x, ar, br = self.linear_interpolate( x , y )
            p3 = self.plot(linear_x, linear_y, logx, logy, True, False)
            ps.append( p3 ) 
            ps_leg.append( "Lfit  %.3f * x^%.3f " % (10.0**br,ar,) )
	    #ps_leg.append( "Lin. fit x^%.3f" % (ar) )

        self.legend(ps, ps_leg)
        #plt.legend(ps, ps_leg)
        
        return x, y
    
    
    def legend(self, plots, plots_legends):
        
	# best        
	plt.legend( plots, plots_legends, loc=0, prop={'size':'x-small'} )
	#plt.legend( plots, plots_legends, loc=3 )
        
    
    def linear_interpolate( self, x , y ):
            
        new_x, new_y = [], []
        for x_i, y_i in zip(x,y):
            if y_i > 0.0:
                new_x.append( x_i )
                new_y.append( y_i )
                
        x, y = new_x, new_y
        
        half_x = x[len(x)/4:-len(x)/4]
        half_y = y[len(y)/4:-len(y)/4]
        
        arrayx = np.ndarray(len(half_x))
        for val, i  in zip(half_x,range(len(half_x))):
            arrayx[i] = math.log10(val)

        all_arrayx = np.ndarray(len(x))
        for val, i  in zip(x,range(len(x))):
            all_arrayx[i] = math.log10(val)

        arrayy = np.ndarray(len(half_y))
        for val, i  in zip(half_y,range(len(half_y))):
            arrayy[i] = math.log10(val)
        
        (ar,br)=polyfit(arrayx,arrayy,1)
        xr=polyval([ar,br],all_arrayx)

        return map(lambda val : 10.0**val, xr), map(lambda val : 10.0**val, all_arrayx), ar, br


    def dist_plot_2d(self, x, y, bins, log_bins, logx=False, logy=False, lines=True, dots=True):
        
        detailed_y, detailed_x, y_err = self.raw_hist_data_2d(x, y) #self.native_hist( sample, len(set(sample)), False)
        
        #x, y = self.log_bins2(sample, bins)
        y, x, _ = self.native_hist_2d( x, y, bins, log_bins)
        x = self.histogram_interpolate(x)
                        
        ps, ps_leg = [], []
        
        p2 = self.plot(detailed_x, detailed_y, logx, logy, False)
        ps.append( p2 ) 
        ps_leg.append( "Complete histogram" )

        p1 = self.plot(x, y, logx, logy, True, True)
        ps.append( p1 ) 
        ps_leg.append( "Hist. log. bin." )
        
        if self.interpolate:
            linear_y, linear_x, ar, br = self.linear_interpolate( x , y )
            p3 = self.plot(linear_x, linear_y, logx, logy, True, False)
            ps.append( p3 ) 
            ps_leg.append( "Lfit %.3f * x^%.3f" % (10.0**br,ar,) )
	    #ps_leg.append( "Linear fit x^%.3f" % (ar) )

        self.legend(ps, ps_leg)
        
        return x, y


    def init_complete_analysis(self, graph, dst_folder, sample_size=10000, bins=10, seed=666, list_of_params=None):
        '''
        list_of_params : possible include 
                              'degree', 
                              'clustering',
                              'knn',
                              'kcore',
                              'triangles',
                              'eccentricity',
                              'path_len',
                              'scaling',
                              'connectivity',
                              'linksphere1',
                              
                        or None for all of them.
        '''
        
        if not list_of_params:
            list_of_params = {
                              'degree' : 10,
                              'clustering' : 10,
                              'knn' : 10,
                              'kcore' : 10,
                              'eccentricity' : 10,
                              'path_len' : 10,
                              'scaling' : 10,
                              'connectivity' : 10,
                              }

        self.list_of_params = list_of_params
        self.dst_folder = dst_folder
        self.bins = bins
        
        try:
            os.makedirs(os.path.abspath(dst_folder))
        except:
            pass
           
        if str(graph.__class__) == '<class \'cloudlight.classes.graph.Graph\'>':
            self.is_big_graph = False
        else:
            self.is_big_graph = True
            
        if self.is_big_graph:
        
            try:
                #graph.create_index_degree()
		pass
            except:
            	print 'WARNING: index for degree already exists!'
            try:
                #graph.create_index_knn()
		pass
            except:
            	print 'WARNING: index for knn already exists!'
            try:
                #graph.create_index_clustering()
		pass
            except:
                print 'WARNING: index clustering already exists!'
            try:
                #graph.create_index_kcores()
		pass
            except:
                print 'WARNING: index kcore already exists!'
            try:
                #graph.create_index_triangles()
		pass
            except:
                print 'WARNING: index kcore already exists!'

            nodes = open(os.path.abspath(dst_folder) + '/nodes.txt').readlines()
            nodes = [l.strip() for l in nodes if l.strip()!='']
            graph.max_nodes_analysis = len(nodes)
                                
            #graph.max_nodes_analysis = graph.number_of_nodes()
            #nodes = list(graph.nodes_iter() )
            #nodes.sort()
            
        else:            
            graph.max_nodes_analysis = sample_size        
            random.seed(seed)
            nodes = graph.random_nodes(sample_size)
        
            nodes_file = open(os.path.abspath(dst_folder) + '/nodes.txt', 'w')
            for node in nodes:
                nodes_file.write('%s\n' % str(node))
            nodes_file.close()
        
        if self.debug:
            print 'INFO: complete graph analysis, sample size = %d , number of bin = %d' % (sample_size, bins)

        analysis_file = open(os.path.abspath(dst_folder) + '/analysis.txt', 'w')
        analysis_file.write('NODES: %d\n' % graph.number_of_nodes())
        analysis_file.write('EDGES: %d\n' % graph.number_of_edges())
        analysis_file.write('NODE_SAMPLE_SIZE: %d\n' % sample_size)
        analysis_file.write('NUMBER_OF_BINS_IN_PLOT: %d\n' % bins)
        analysis_file.close()

        self.nodes = nodes

    
    def complete_analysis(self, graph):

        nodes = self.nodes
        list_of_params = self.list_of_params
        
        if 'degree' in list_of_params:
                        
            if self.is_big_graph:                
                node_degree = list( graph.get_parameter_cache_iter('degree') )
                node_degree.sort( lambda x, y : cmp( x[0], y[0] ) )
                iter_func = lambda x : (d for _,d in node_degree)
            else:
                iter_func = graph.degrees_iter
            self.degrees = self.__analysis_save(iter_func, 'degree', graph, nodes)
                
        if 'clustering' in list_of_params:

            if self.is_big_graph:
                node_clusts = list( graph.get_parameter_cache_iter('clustering') )
                node_clusts.sort( lambda x, y : cmp( x[0], y[0] ) )
                iter_func = lambda x : (c for _,c in node_clusts)
            else:
                iter_func = graph.clustering_indices_iter

            self.clusts = self.__analysis_save(graph.clustering_indices_iter, 'clustering', graph, nodes)

                
        if 'knn' in list_of_params:

            if self.is_big_graph:
                node_knns = list( graph.get_parameter_cache_iter('knn') )
                node_knns.sort( lambda x, y : cmp( x[0], y[0] ) )
                iter_func = lambda x : (k for _,k in node_knns)
            else:
                iter_func = graph.average_neighbor_degrees_iter

            self.knns = self.__analysis_save(graph.average_neighbor_degrees_iter, 'knn', graph, nodes)                


#        if 'linksphere1' in list_of_params:
#
#            self.linksphere1 = open(os.path.abspath(self.dst_folder)+'/linksphere1.txt').readlines()
#            self.linksphere1 = map(float, self.linksphere1)

        if [param for param in list_of_params if 'sphere' in param] != []:
            for lookahead in range(1,4):
                #try:
                type = 'node'
                self.nodesphere = []
                self.nodesphere.append( self.__analysis_save(lambda ns : graph.nodesphere_iter(ns,lookahead), '%ssphere%d'%(type,lookahead), graph, nodes) )
                #except:
                #print 'Warning: parameter %s no available...' % ('%ssphere%d'%(type,lookahead))
                #try:
                type = 'link'
                self.linksphere = []
                self.linksphere.append( self.__analysis_save(lambda ns : graph.linksphere_iter(ns,lookahead), '%ssphere%d'%(type,lookahead), graph, nodes) )
                #except:
                #    print 'Warning: parameter %s no available...' % ('%ssphere%d'%(type,lookahead))

        if 'kcore' in list_of_params:
            self.kcores = self.__analysis_save(graph.kcoreness_iter, 'kcore', graph, nodes)
        if 'eccentricity' in list_of_params:
            self.eccs = self.__analysis_save(graph.eccentricities_iter, 'eccentricity', graph, nodes)
        if 'path_len' in list_of_params:
            self.path_lens = self.__analysis_save(graph.average_path_lengths_iter, 'path_len', graph, nodes)
        if 'scaling' in list_of_params:
            self.scalings = self.__analysis_save(graph.max_internal_scaling_iter, 'scaling', graph, nodes)
            self.scaling_lists = self.__analysis_save(graph.internal_scaling_iter, 'scaling_list', graph, nodes)
        if 'connectivity' in list_of_params:
            self.conns = self.__analysis_save(graph.max_connectivity_iter, 'connectivity', graph, nodes)
            self.conn_lists = self.__analysis_save(graph.connectivity_iter, 'connectivity_list', graph, nodes)
                        
        
    def plot_graph_params(self):
        '''
        To be called after complete_analysis().
        '''

        # 1D

        for param in self.param_label:
            
            if param in self.list_of_params:

                self.interpolate = self.param_interpolate[param]                
                self.plot_graph_param(
                                      param, self.param_title[param], 
                                      '%s : %s' % (self.param_variable[param],self.param_label[param]),
                                      'P(%s)'%self.param_variable[param],
                                      self.param_log_bins[param],
                                      self.param_logx[param], 
                                      self.param_logy[param],
                                      )
        
        self.interpolate = True

        # 2D

        for param1 in self.param_title:
            
            for param2 in self.param_title:
    
		p1, p2 = param1, param2
                if p1 in self.list_of_params and p2 in self.list_of_params and p1 < p2:
                    
                    self.plot_graph_param_2d(
                            p1, 
                            p2, 
                            '%s vs %s' % (self.param_label[p1],self.param_label[p2],), 
                            '%s : %s' % (self.param_variable[p1],self.param_label[p1]),
                            '%s : %s' % (self.param_variable[p2],self.param_label[p2]),
                            self.param_log_bins[p1],
                            self.param_logx[p1], 
                            self.param_logy[p2],
                            )
                    # the same in different order
                    p1, p2 = p2, p1
                    self.plot_graph_param_2d(
                            p1, 
                            p2, 
                            'Distribution of %s vs %s' % (self.param_label[p1],self.param_label[p2],), 
                            '%s : %s' % (self.param_variable[p1],self.param_label[p1]),
                            '%s : %s' % (self.param_variable[p2],self.param_label[p2]),
                            self.param_log_bins[p1],
                            self.param_logx[p1], 
                            self.param_logy[p2],
                            )
                


        # list parameters
    
        if 'scaling' in self.list_of_params:
            self.plot_graph_param_list('scaling', 'internal scaling', 'd : distance to node', 's : internal scaling', False, False, False)

        if 'connectivity' in self.list_of_params:
            self.plot_graph_param_list('connectivity', 'connectivity', 'd : distance to node', 'c : connectivity', False, False, False)



    def plot_graph_param_list(self, param, title, x_label, y_label, log_bins, x_log, y_log):
        
        self.title = title
        self.x_label = x_label
        self.y_label = y_label
        
        data = open(os.path.abspath(self.dst_folder) + '/%s_list.txt' % param).readlines()
        data = [line.strip() for line in data]
        data_aux = []
        for string in data:
            l = eval(string)
            data_aux.append( l )
        data = data_aux
        
        x, y = self.list_of_lists_to_2d(data)
        
        x_aux, y_aux = [],[]
        for x_i, y_i in zip(x,y):
            if y_i > 0.0:
                x_aux.append( x_i )
                y_aux.append( y_i )
        x = x_aux
        y = y_aux
        #x = [x_i  for x_i, y_i in zip(x,y) if y_i > 0.0]
        #y = [y_i  for x_i, y_i in zip(x,y) if y_i > 0.0]
        
        
        # with binning
        self.title = 'Scattering and Average ' + title        
        self.clear()
        detailed_y, detailed_x, y_err = self.raw_hist_data_2d(x, y)        
        self.plot(x, y, x_log, y_log, False, True)         
        #self.plot(detailed_x, detailed_y, x_log, y_log, True, True)
        
        plt.errorbar(detailed_x, detailed_y, y_err, barsabove=True, capsize=5)

        self.save(os.path.abspath(self.dst_folder) + '/%s_list.eps' % param)
        self.save(os.path.abspath(self.dst_folder) + '/%s_list.png' % param)
        
    
    
    
    def plot_graph_param(self, param, title, x_label, y_label, log_bins, x_log, y_log):
        
        if self.debug:
        	print 'INFO: plotting parameter %s ...' % param
        
        self.title = title
        self.x_label = x_label
        self.y_label = y_label
        
        data = open(os.path.abspath(self.dst_folder) + '/%s.txt' % param).readlines()
        data = [float(line.strip()) for line in data]
        
        self.clear()
        self.dist_plot(data, self.list_of_params[param], log_bins, x_log, y_log,) 
        self.save(os.path.abspath(self.dst_folder) + '/%s.eps' % param)
        self.save(os.path.abspath(self.dst_folder) + '/%s.png' % param)
    
        
    def plot_graph_param_2d(self, param1, param2, title, x_label, y_label, log_bins, x_log, y_log):
        
        if self.debug:
        	print 'INFO: plotting parameters %s and %s ...' % (param1, param2)
        
        self.title = title
        self.x_label = x_label
        self.y_label = y_label
        
        data1 = open(os.path.abspath(self.dst_folder) + '/%s.txt' % param1).readlines()
        data1 = [float(line.strip()) for line in data1]
        
        data2 = open(os.path.abspath(self.dst_folder) + '/%s.txt' % param2).readlines()
        data2 = [float(line.strip()) for line in data2]

        self.clear()
        self.dist_plot_2d(data1, data2, self.list_of_params[param1], log_bins, x_log, y_log,) 
        self.save(os.path.abspath(self.dst_folder) + '/%s-%s.eps' % (param1,param2))
        self.save(os.path.abspath(self.dst_folder) + '/%s-%s.png' % (param1,param2))
    
        
    def __analysis_save(self, iter_func, name, graph, nodes):

        if self.debug:
            print 'INFO: computing %s...' % name

        file = open(os.path.abspath(self.dst_folder) + '/%s.txt'%name, 'w')
        param_list = []
        count = 0        
        for val, node in izip( iter_func(nodes), nodes):
                param_list.append( val )
                file.write('%s\n' % str(val))
                file.flush()
                if self.debug and count % 10000 == 0:
                    print 'INFO: %s %s for node %s computed (%d of %d).' % (name, str(val), str(node), len(param_list), len(nodes) )
                count += 1
        file.close()
        
        return param_list
        

    def list_of_lists_to_2d(self, list):
        
        x, y = [], []
        
        for l in list:
            
            for elem, i in zip(l, range(len(l))):
                
                x.append( i )
                y.append( elem  )
                
        return x, y
    
    
