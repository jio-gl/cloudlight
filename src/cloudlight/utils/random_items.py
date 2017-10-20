'''
Created on Mar 19, 2010

@author: jose

original source from:
http://groups.google.com/group/networkx-discuss/browse_thread/thread/a87dd6ca7063a778?pli=1
'''

from random import *

def random_items(iterable, k=1):
    # Raymond Hettinger's recipe
    # http://code.activestate.com/recipes/426332/
    result = [None] * k
    for i, item in enumerate(iterable):
        if i < k:
            result[i] = item
        else:
            j = int(random() * (i + 1))
            if j < k:
                result[j] = item
    shuffle(result)
    return result 
