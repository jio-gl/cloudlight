# cloudlight

A library extending NetworkX with SQLite databases for analyzing complex networks like social networks.


# Dependencies:

* NetworkX 1.0.1 or above (http://networkx.lanl.gov/).

* (optional) Matplotlib for graph plotting (sudo apt-get install python-matplotlib) for:
 * classes.graph.Graph.show()
 * utils.plot

* (optional) SimpleJSON for Python (http://pypi.python.org/pypi/simplejson/) for:
 * nodes.twitter

* (optional) python-mechanize (http://wwwsearch.sourceforge.net/mechanize/) for:
 * nodes.facebook

* (optional) python-numpy (http://numpy.scipy.org/) for:
 * algorithms.plot

* (optional) python-scipy (sudo apt-get install python-scipy) for interpolation in:
 * algorithms.plot

* (optional) sqlite3 (sudo apt-get install sqlite3) for class BigGraph in:
 * classes.big_graph
