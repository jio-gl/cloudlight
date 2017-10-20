'''
Created on Apr 9, 2010

@author: jose
'''

import re, urllib2


class UrlNode(object):
    '''
    classdocs
    '''
    
        
    url_regex = '((https?|ftp|gopher|telnet|file|notes|ms-help):((//)|(\\\\))+[\w\d:#@%/;$()~_?\+-=\\\.&]*)'
    

    def getUrl(self):
        return self.__url


    def setUrl(self, url):
        matches = re.findall( self.url_regex, url)
        if len(matches) == 0:
            raise Exception('ERROR: malformed url attribute of node instance of class LinkNode!')
        
        self.__url = url


    def delUrl(self):
        del self.__url

    
    def __init__(self, url):
        '''
        Constructor
        '''
        self.url = url
    url = property(getUrl, setUrl, delUrl, "Url's Docstring")


    def protocol(self):
        
        return self.url.split(':')[0]
    
    
    def domain(self):
        
        if '//' in self.url:
            
            return self.url.split('//')[1].split('/')[0]
        
        else:
            
            return self.url.split('\\\\')[1].split('\\')[0]


    def resource(self):
        
        if '//' in self.url:
            
            res = self.url.split('//')[1].split('/')            
            return '/' + '/'.join(res[1:])
        
        else:
            
            res = self.url.split('\\\\')[1].split('\\')            
            return '\\' + '\\'.join(res[1:])


    def data(self):
        
        return urllib2.urlopen(self.url).read()



if __name__ == '__main__':
    
    myurl = UrlNode('http://tuplets.org')
    print myurl.protocol()
    print myurl.domain()
    print myurl.resource()
    
    myurl = UrlNode('http://www.search.com/search?q=zarasa%20bla')
    print myurl.protocol()
    print myurl.domain()
    print myurl.resource()
    