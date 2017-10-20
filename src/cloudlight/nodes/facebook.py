#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

from mechanize import Browser
import mechanize
import urllib2, urllib
import re, time

from threading import Lock

from cloudlight.bots.visitor import Visitor
from cloudlight.classes.graph import Graph

class Callable:
    def __init__(self, anycallable):
        self.__call__ = anycallable



class Link:
    absolute_url = None


from cloudlight.nodes.node import Node

class FacebookNode(Node):

    debug = False

    def __init__(self, id=None, name=None):
        '''
        Constructor
        '''

        super(FacebookNode, self).__init__()
        
        if not name and not id:
            raise Exception('no Facebook name or Facebook id specified!')
        
        self.name = name
        self.id = id
        
        
    def __repr__(self):
        return str(self.id)    
    
        
class FacebookBrowser(object):
        
    @classmethod
    def initialize(cls, proxies_per_proto={}, user=None, passw=None, debug=False):
        
        cls.__br = Browser()
        cls.__br.set_proxies(proxies_per_proto)
        cls.__br.set_debug_http(debug)
        
        # no handling of robots.txt to avoid extra GETs.
        cls.__br.set_handle_robots(False)

        try:
            # sign in
            cls.__br.open("http://www.facebook.com/login.php")
            cls.__br.select_form(nr=0)
            cls.__br['email'] = user
            cls.__br['pass'] = passw
            resp = cls.__br.submit()

            time.sleep(2.0)
            
            cls.__good = True
            
        except Exception, e:
            print str(e)	
            print 'EXCEPTION on FacebookBot, possibly bad user/password or https login don\' work behind a proxy.'
            cls.__good = False


    def set_proxies_per_proto(self, proxies):
        self.__br.set_proxies(proxies)       



    def __repr__(self):

        return str(self.name or self.id)


    def __str__(self):

        return str(self.name or self.id)


    def search(self, query):

        time.sleep(2.0)
        
        url_query = urllib.urlencode({'q':query})
        link = Link()
        link.absolute_url = 'https://www.facebook.com/search/?' + url_query

        resp = self.__br.follow_link(link)
        cont = resp.read()

        links = re.findall("addfriend.php\?id=[0-9]+", cont)

        links = list(set(map(lambda x: x.split('=')[-1], links)))

        links_urls = []
        for link in links:
            links_urls.append(link)
        
        return links_urls


    def friends(self, node, max=5000):

        time.sleep(2.0)

        if node.id:
            return self.__impl_friends(node.id, max)
        else:
            ids = self.search(node.name)
            if len(ids) != 1:
                raise Exception('Facebook search for "%s" resulted in %d results. Only works with ONE result!' % (node.name, len(ids)))
            else:
                node.id = ids[0]
                return  self.__impl_friends(node.id, max)
        
    
    def __impl_friends(self, id, max=5000):

        # retrieve the first n (how many?) contacts as tuples (complete_name, facebook_url).
        full_url = 'http://www.facebook.com/friends/?id=%d' % id
        resp = self.__br.open( full_url )
        cont =  resp.read()

        open('friends.html','w').write(cont)

        ids = re.findall('ConnectDialog\(\&quot;[0-9]+', cont)
        ids = list(set(map(lambda x: int(x.split(';')[-1]), ids)))
        ids.sort()
        
        nodes = map(lambda x : FacebookNode(id=x), ids[:max])
        return nodes


    def add_friends(self, graph, max=5000, grab_user_details=True):
        '''
        Adds to the graph the friends of the node.
        '''
        nodes = self.friends(max)
        
        if grab_user_details:
            map(lambda x: x.grab_user_details(), nodes)
            
        graph.add_edges_from( map(lambda x : (self, x), nodes) )        


    def visit_friends(self):
        '''
        '''
        nodes = self.friends()
        return [], map(lambda x : (self, x), nodes)


    def grab_user_details(self):
        '''
        detailed user info
        '''

        time.sleep(2.0)

        if not self.id:
            ids = self.search(self.name)
            if len(ids) != 1:
                raise Exception('Facebook search for "%s" resulted in %d results. Only works with ONE result!' % (self.name, len(ids)))
            else:
                self.id = ids[0]

        full_url = 'http://www.facebook.com/profile.php?id=%d' % self.id
        resp = self.__br.open( full_url )
        cont =  resp.read()        
        
        names = re.findall('people\/[a-zA-Z-_áéíóú]+', cont)
        if len(names) == 0:
            names = re.findall('<title>[a-zA-Z -_\.áéíóú]+ \| Facebook</title>', cont)
        if len(names) == 0:
            names = re.findall('<title>Facebook \| [a-zA-Z -_\.áéíóú]+</title>', cont)

        if len(names) >= 1:
            self.name = names[0].replace('<title>','').replace('</title>','').replace('Facebook','').replace(' | ','').replace('people','').replace('/','').replace('-',' ')
        else:
            raise Exception('Facebook user title/name not found in FacebookNode.grab_user_details()')



class FacebookFriendVisitor(Visitor):


    def setFacebookBrowser(self, fb_browser):
        
        self.facebook_browser = fb_browser


    def visitFacebookNode(self, node, *args):
        
        print 'Visitando nodo facebook: id = %s, name = %s' % (node.id, node.name)
    
        fb_local_graph = Graph()
        
        friends = self.facebook_browser.friends(node)
        for f in friends:
            print node, f
            fb_local_graph.add_edge(node, f)
            
        return fb_local_graph

