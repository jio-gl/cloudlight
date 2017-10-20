#
#     This file is part of the Cloudlight project. 
#     Copyright (c) 2010  Jose Ignacio Orlicki. Some rights reserved.
#     For details read https://www.assembla.com/code/cloudlight/subversion/nodes/LICENSE
#    
#     The code in this file is based on distance.py, nsed.py and nsedthread.py from Exomind v0.2
#     Exomind-v0.2 (OLD VERSION)      DOWNLOAD      .zip      27-11-2008
#     http://corelabs.coresecurity.com/index.php?module=Wiki&action=attachment&type=tool&page=Exomind&file=Exomind-v0.2.zip
#    
#     We include the original copyright notice to comply with the Apache-type open-source license:
#    
#     Copyright (c) 2008 Core Security Technologies.  All rights
#     reserved.
#     
#    Redistribution and use in source and binary forms, with or without
#    modification, are permitted provided that the following conditions
#    are met:
#    
#    1. Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#    
#    2. Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in
#       the documentation and/or other materials provided with the
#       distribution.
#    
#    3. The end-user documentation included with the redistribution,
#       if any, must include the following acknowledgment:
#          "This product includes software developed by
#           CORE Security Technologies (http://www.coresecurity.com/)."
#       Alternately, this acknowledgment may appear in the software itself,
#       if and wherever such third-party acknowledgments normally appear.
#    
#    4. The names "Exomind" and "CORE Security Technologies" must
#       not be used to endorse or promote products derived from this
#       software without prior written permission. For written
#       permission, please contact oss@coresecurity.com.
#    
#    5. Products derived from this software may not be called "Exomind",
#       nor may "Exomind" appear in their name, without prior written
#       permission of CORE Security Technologies.
#    
#    THIS SOFTWARE IS PROVIDED ``AS IS'' AND ANY EXPRESSED OR IMPLIED
#    WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
#    OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#    DISCLAIMED.  IN NO EVENT SHALL CORE SECURITY TECHNOLOGIES OR
#    ITS CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#    SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#    LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF
#    USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
#    ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
#    OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT
#    OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
#    SUCH DAMAGE.
#


import httplib, urllib
import re
import math
import pickle


# thread imports
from threading import Thread


class QueryThread(Thread):
    
    _proxy_conn = None
    
    def __init__ (self, nsed, pairs, context=''):

        Thread.__init__(self)
        
        self.status = -1
        
        self.__nsed = nsed
        self.__pairs = pairs
        self.context = context
        self.distances = {}
       
      
    def run(self):
        
        # now False, to not use threads.
        self.distances = self.__nsed.distances(self.__pairs, self.context, False)



class Cache:

    def __init__(self, max_size=1000):
        
        self.__max = max_size
        self.__dict = {}
        
        
    def __getitem__(self, key):

        try:
            item = self.__dict[key]
        except:
            item = None
            
        return item
    
    
    def __setitem__(self, key, item):
        
        if not key in self.__dict and len(self.__dict) >= self.__max:
            # remove one
            del self.__dict[ list(self.__dict.keys())[0] ]
            
        self.__dict[key] = item
        
        
    def has_key(self, key):
        
        return self.__dict.has_key(key)
    
    
    def __str__(self):
        
        return str(self.__dict)
    
    
    def keys(self):
        
        return self.__dict.keys()


class QueryResultNode:

    def __init__(self, link, cache_link, snippet, title):
        
        self.title = title
        self.link = link
        self.cache_link = cache_link
        self.snippet = snippet


    def __str__(self):

        return str((self.title, self.link, self.cache_link, self.snippet))


# Normalized Search Engine Distance
class QueryNode(object):


    def query(self):
        
        string = self.search_string
        
        ret = []

        links = self.links_query(string)
        cache_links = self.links_cache_query(string)
        snippets = self.snippets_query(string)
        titles = self.titles_query(string)

        for i in range(len(links)):
            ret.append(QueryResultNode(links[i], cache_links[i], snippets[i], titles[i]))
        return ret


    def add_results(self, graph):
        
        nodes = self.query()
            
        graph.add_edges_from( map(lambda x : (self, x), nodes) )        
    
                    
    # avoid unescaped double quotes in string
    def update_results_query(self):

        self.results = self.__results(self.search_string)
        

    # quotes are not implicit in context, but are in x and y.
    def node_distance(self, nodeA, nodeB, context=None):

        return self.distance((nodeA.search_string, nodeB.search_string), context)


    def __search_engine_strip(self):
        return ''

    @classmethod
    def __load_cache(cls):

        # experimental persistent cache.
        try:

            pkl_file = open('QueryFactory.cache', 'rb')
            cache = pickle.load(pkl_file)
            pkl_file.close()
        except:
            cache = Cache()
            
        return cache
    
    
    @classmethod    
    def save_cache(cls):
        
        output = open('QueryFactory.cache', 'wb')
        
        # Pickle dictionary using protocol 0.
        pickle.dump(cls.__cache, output)
        
        output.close()
        
        
    def __init__(self, url, get, regex, strip, params, qparam):

        self.__base = 2
        self.__start = 0
        self.__num = 100
        self.__failures = 0
        self.__debug = False
        self.__use_cache = True
        
        self.__url = url
        self.__get = get
        self.__regex = regex
        self.__strip = strip
        self.__params = params
        self.__qparam = qparam
        
        self.__cache = self.__load_cache()
        self.set_context('')

        self.search_string = None
        self.results = None
        


    @classmethod
    def initialize(cls, proxies):
        
        cls.set_proxies(proxies)
        


    @classmethod
    def set_proxies(cls, proxies=None):
        '''
        Using one proxy connection per class, not per instance.
        '''
        
        cls.__proxies = proxies
        if proxies and 'http' in proxies:

            host = proxies['http'].split(':')[0]
            port = proxies['http'].split(':')[1]
            
            try:
                cls._proxy_conn = httplib.HTTPConnection(host, int(port))
                cls._proxy_conn.connect()
            except:
                cls._proxy_conn = None
                
        else:
            
            cls._proxy_conn = None


    def set_sleep_secs(self, secs):

        self.__sleep_secs = float(secs)


    def set_sleep_module(self, iterations):

        self.__sleep_module = iterations


    def set_sleep_failure(self, secs):

        self.__sleep_failure = float(secs)        


    def set_sleep_random_flag(self, bool):

        self.__sleep_random_flag = bool        


    def set_use_cache(self, bool):

        self.__use_cache = bool        


    def set_debug(self, bool):

        self.__debug = bool        


    def update_params(self, key, val):

        self.__params[key] = val


    def clear_failures(self):

        self.__failures = 0


    def get_failures(self):

        return self.__failures


    def set_context(self, context):

        self.context = context
        # results for letter 'a' as approximation of total pages indexed
        self.__total = self.__results('a', context)


    def get_context(self):

        return self.context


    def get_base(self):

        return self.__base


    def results_total(self):

        return self.__total


    def __add_quotes(self, str):

        if str.find(' ') != -1 and len(str) > 0 and str[0] != '"' and str[-1] != '"':
            return '"' + str + '"'
        else:
            return str


    # quotes are not implicit in context, but are in string
    def __results(self, string, context=None):

        if context and context != self.context:
            self.set_context(context)
        else:
            context = self.context        

        if context != self.context:
            self.set_context(context)

        res = self.__results_list([string, context])
        return res 


    # avoid unescaped double quotes in string
    def __results_query(self, string):

        # first check cache
        ms = self.__matches_query(string)

        if len(ms) == 0:
            res = 0
            self.__failures += 1
        else:            
            res = long(ms[0])
        
        return res
        

    def __strip_link(self, link):

        link = link.group()
        return link[9:-9]


    def __strip_link_cache(self, link):

        link = link.group()
        return link[9:]


    def __strip_snippet(self, snippet):

        snippet = snippet.group()
        return snippet[15:-4]


    def __strip_title(self, title):

        title = title.group()
        return title[8:-4]


    def links_query(self, num=100, start=0):

        string = self.search_string

        self.__params['start'] = start
        self.__params['num'] = num
        
        #ret = self.__matches_query(string, '<a href="http://[\+a-zA-Z./0-9\?\_=&,;%-]+" class=l', self.__strip_link)
        ret = self.__matches_query(string, '<a href="((https?|ftp|gopher|telnet|file|notes|ms-help):((//)|(\\\\))+[\w\d:#@%/;$()~_?\+-=\\\.&]*)" class=l', self.__strip_link)
        ret = map(lambda x : x.replace('&amp;', '&'), ret)
        
        self.__params['num'] = 1
        return ret


    def links_cache_query(self, num=100):

        string = self.search_string

        self.__params['num'] = num
        
        ret = self.__matches_query(string, '<a href="http://[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+/search\?q=cache:[\+a-zA-Z./0-9\?\_=&,;%:]+', self.__strip_link_cache)
        
        self.__params['num'] = 1
        return ret


    def snippets_query(self, num=100):
        
        string = self.search_string
        
        self.__params['num'] = num

        ret = self.__matches_query(string, '<div class="s">([^<]*(<b>)*(</b>)*(<em>)*(</em>)*)*<br>', self.__strip_snippet)
        
        self.__params['num'] = 1
        return ret


    def titles_query(self, num=100):
        
        string = self.search_string
        
        self.__params['num'] = num

        ret = self.__matches_query(string, 'class=l>([^<]*(<b>)*(</b>)*(<em>)*(</em>)*)*</a>', self.__strip_title)
        
        self.__params['num'] = 1
        return ret


    def __do_req(self, string):        

        url_string = string + ' ' + self.__add_quotes(self.context)

        # don't forget to strip blank spaces
        self.__params[self.__qparam] = url_string.strip()
        #self.__params['start'] = self.__start
        url_params = urllib.urlencode(self.__params)

        full_url = 'http://' + self.__url + self.__get + url_params

        if not self.__class__._proxy_conn:
            self.conn = httplib.HTTPConnection(self.__url)        
            self.conn.request("GET", self.__get + url_params)
        else: # use one proxy connection per class, not per instance
            self.conn = self.__class__._proxy_conn            
            self.conn.request("GET", full_url)

        if self.__debug:
            print 'http://' + self.__url + self.__get + url_params 

        r1 = self.conn.getresponse()        
        p = r1.read()
        
        # remove qparam to avoid confusing the cache on __matches_query()
        del self.__params[self.__qparam]
        
        return p


    # avoid unescaped double quotes in string
    def __matches_query(self, string, regex=None, strip=None):

        string = string.strip()

        key = str((string, urllib.urlencode(self.__params)))
        if self.__cache.has_key(key):
            p = self.__cache[key]
        else:
            p = self.__do_req(string)
            self.__cache[key] = p

        if not regex:
            regex = self.__regex
            strip = self.__strip
        
        iterator = re.finditer(regex, p)
        ret = []
        for match in iterator:
            ret.append(strip(match))
        
        return ret


    def __results_list(self, list):

        string = ''
        for s in list:
            string += self.__add_quotes(s) + ' '

        return self.__results_query(string)
    
    
    def only_entropy(self, string, context=None):
        
        _, _, norm_ent = self.entropy(string, context)        
        return norm_ent
    
    
    def only___results(self, string, context=None):
        
        res, _, _ = self.entropy(string, context)
        return res
    
    
    # return num_hits, entropy, normalized_entropy
    def entropy(self, string, context=None):

        if context and context != self.context:
            self.set_context(context)
        else:
            context = self.context
        
        results = self.__results(string, context)

        if results != 0:
            
            ent = -math.log(float(results) / self.__total, self.__base)
            max_ent = self.__max_entropy(context)
            norm_ent = (max_ent - ent) / max_ent
            ent = max_ent - ent 
        
        else:

            ent, norm_ent = 0.0, 0.0
        
        return results, ent, norm_ent


    def __max_entropy(self, context=None):

        if context and context != self.context:
            self.set_context(context)
        else:
            context = self.context        

        return - math.log(1.0 / self.__total, self.__base)


    def max_entropy(self):

        return 1, self.__max_entropy(), 1.0


    def min_entropy(self):

        return self.results_total(), 0.0, 0.0


    # quotes are not implicit in context, but are in x and y.
    def distance(self, (x, y), context=None):

        return self.__distance((x, y), context, self.__norm_se_dist)


    def jaccard_distance(self, (x, y), context=None):

        return self.__distance((x, y), context, self.__jaccard_dist)


    def hits_distance(self, (x, y), context=None):

        return self.__distance((x, y), context, self.__hits_dist)


    def __distance(self, (x, y), context=None, func=None):

        if context and context != self.context:
            self.set_context(context)
        else:
            context = self.context
        
        x_res = self.__results(x, context)
        y_res = self.__results(y, context)
        # x,y results as a set, not concatenation
        xy_res = self.__results_list([x, y, context])

        # use base 2 logs to compute final value
        return func(x_res, y_res, xy_res, self.__total, self.__base)
    
    
    def __norm_se_dist(self, x_res, y_res, xy_res, total, base):

        if x_res == 0 or y_res == 0 or xy_res == 0:
            return None
        
        base = self.__base
        numerator = max(math.log(x_res, base), math.log(y_res, base)) - math.log(xy_res, base)
        denominator = math.log(total, base) - min(math.log(x_res, base), math.log(y_res, base))
        
        ret = numerator / denominator
        return ret 


    def __jaccard_dist(self, x_res, y_res, xy_res, total, base):

        if x_res == 0 and y_res == 0:
            return None

        if xy_res == 0:
            return None # assume equal

        numerator = xy_res
        denominator = x_res + y_res - xy_res

        if denominator > 0:
            ret = float(numerator) / denominator
        else:
            ret = 0.0

        return ret 


    def __hits_dist(self, x_res, y_res, xy_res, total, base):

        return xy_res


    def distances(self, pairs, context=None, use_threads=True):

        if context and context != self.context:
            self.set_context(context)
        else:
            context = self.context
        
        if use_threads:
            return self.__fast_distances(pairs, context)
        else:
            dists = {}
            for p in pairs:
                dists[p] = self.distance(p, context)
            return dists


    def __fast_distances(self, pairs, context=''):
        dists = {}
        threads = 8
        size = 8
    
        partial = 0
        while partial < len(pairs):
    
            threadlist = []
            thread_count = 0
            while thread_count < threads and partial < len(pairs):

                thread_instance = QueryNode(self.__url, self.__get, self.__regex, self.__strip, self.__params, self.__qparam, self.__cache)
                
                current = QueryThread(thread_instance, pairs[partial:partial + size], context)
                
                partial += size
                threadlist.append(current)
                current.start()
                thread_count += 1
    
            for thread in threadlist:
                thread.join()
                dists.update(thread.distances)
    
        return dists
               
   
# Normalized Google Search Distance
class GoogleQueryNode(QueryNode):

    _proxy_conn = None

    def __google_strip(self, match):

        s = match.group().replace('about ', '')
        return s[len('swrnum='):-len('"')].replace(',', '')

    def __init__(self, proxies=None):

        url = 'www.google.com'
        get = '/search?'
        params = {}
        params['num'] = '1'
        params['filter'] = '0'
        params['start'] = '0'
        params['btnG'] = 'Search'
        params['hl'] = 'en'        
        qparam = 'q'
        #regex = '</b> of about [0-9,]+</b> for <b>'
        regex = 'swrnum=[0-9]+"'
        strip = self.__google_strip
        super(GoogleQueryNode, self).__init__(url, get, regex, strip, params, qparam)
        self.__failures = 0
        self.__debug = False



# Normalized Google Groups Distance
class GoogleGroupsQueryNode(QueryNode):

    def __google_groups_strip(self, match):

        s = match.group()
        return s[len('of about <b>'):-len('</b>')].replace(',', '')


    def __init__(self, proxies=None):

        url = 'groups.google.com'
        get = '/groups/search?'
        params = {}
        params['num'] = '1'
        params['qt_s'] = 'Search+Groups'                
        qparam = 'q'
        regex = 'of about <b>[0-9,]+</b>'
        strip = self.__google_groups_strip
        super(GoogleGroupsQueryNode, self).__init__(url, get, regex, strip, params, qparam, proxies)
        self.__failures = 0
        self.__debug = False


# Normalized Msn Search (now Live Search) Distance
class MsnFactory(QueryNode):

    def __msn_strip(self, match):

        return match.group()[len('Page 1 of '):-len(' results</span>')].replace(',', '')


    def __init__(self, proxies=None):

        url = 'search.live.com'
        get = '/results.aspx?'
        params = {}
        params['go'] = ''
        params['form'] = 'QBRE'        
        qparam = 'q'
        regex = 'Page 1 of .* results</span>'
        strip = self.__msn_strip
        super(MsnFactory, self).__init__(url, get, regex, strip, params, qparam, proxies)
        self.__failures = 0



# Normalized Yahoo Search Distance
class YahooQueryNode(QueryNode):


    def __yahoo_strip(self, match):

                return match.group()[len('1 - 10 of '):-len(' for ')].replace(',', '')


    def __init__(self, proxies=None):

        url = 'search.yahoo.com'
        get = '/search?'
        params = {}
        qparam = 'p'
#        <span id="infototal">16900000000</span>
        regex = '1 - 10 of [0-9,]+ for '
        strip = self.__yahoo_strip
        super(YahooQueryNode, self).__init__(url, get, regex, strip, params, qparam, proxies)
        self.__failures = 0


# FotologFactory Harvester
class FotologQueryNode(QueryNode):

    def __fotolog_strip(self, match):
        return match.group()[len('www.fotolog.com/'):-len('/')].replace(',', '')

    def __init__(self):
        url = 'ff.fotolog.com'
        get = '/all.html?p=%s'
        params = {}
        qparam = 'u'
        regex = 'www.fotolog.com\/[a-z0-9_-]+\/'
        strip = self.__yahoo_strip
        super(FotologQueryNode, self).__init__(url, get, regex, strip)
        self.__failures = 0
        

