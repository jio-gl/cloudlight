from cloudlight.classes.graph import Graph
import sys

graph = Graph()

graph.debug = True
graph.input_debug_links = 200000
graph.output_debug_nodes = 100

graph.max_links_input = 5*10**5
graph.max_nodes_analysis = 10000

filename =  len(sys.argv) > 1 and sys.argv[1] or None 

if not filename:
    print 'Error: first argument missing, input filename with space separated graph!'

outname =  len(sys.argv) > 2 and sys.argv[2] or None

if not outname:
    print 'Error: second argument missing, output filename!'

links =  len(sys.argv) > 3 and sys.argv[3] or None

if not links:
    print 'Error: third argument missing, max number of links!'

graph.max_links_input = int(links)

print 'loading graph ' + filename
graph.load_edgelist(open(filename), num=False)

print 'saving giant connected component in %s' % outname
graph.save_bigger_component(outname)



