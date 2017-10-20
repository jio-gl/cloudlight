'''
Created on Mar 18, 2010

@author: jose
'''

import urllib, urllib2, time, base64, random, re, os

import simplejson as json
import twython

from mechanize import Browser

from cloudlight.classes.graph import Graph
from cloudlight.nodes.node import Node
from cloudlight.bots.visitor import Visitor


class TwitterNodeException(Exception):
    pass



class TwitterNode(Node):


    def __init__(self, screen_name=None, num_id=None):
        '''
        Constructor
        '''

        super(TwitterNode, self).__init__()
        
        if not screen_name and not num_id:
            raise Exception('no Twitter screen_name or Twitter num_id specified!')
        
        self.screen_name = screen_name
        self.num_id = num_id
        
        
    def __repr__(self):
        return self.screen_name != None and self.screen_name or str(self.num_id)
        
        
class TwitterBrowser(object):

    debug = False
    base_url = 'http://twitter.com'
    user_url = 'http://api.twitter.com/1/users/show/%s.json'
    screen_name = None

    def __repr__(self):
        
        return str(self.screen_name or self.num_id)


    def __str__(self):
        
        return str(self.screen_name or self.num_id)


    def friends(self, node=None, max=5000):
        if node.screen_name:
            url = 'http://api.twitter.com/1/friends/ids/%s.json' % node.screen_name
        elif node.num_id:
            url = 'http://api.twitter.com/1/friends/ids.json?user_id=%d' % node.num_id
        
        json_string = urllib2.urlopen(url).read()
                
        friends_ids = json.loads(json_string)
        
        nodes = map(lambda x : TwitterNode(num_id=x), friends_ids[:max])
        return nodes        
        
        
    def add_friends(self, graph, max=5000, grab_user_details=True):
        '''
        Adds to the graph the friends of the node.
        ids of friends
        http://apiwiki.twitter.com/Twitter-REST-API-Method%3A-friends%C2%A0ids
        http://api.twitter.com/1/friends/ids/therm000.json 
        '''
        nodes = self.friends(max)
        
        if grab_user_details:
            map(lambda x: x.grab_user_details(), nodes)
            
        graph.add_edges_from( map(lambda x : (self, x), nodes) )        


    def visit_friends(self):
        '''
        Adds to the graph the friends of the node.
        ids of friends
        http://apiwiki.twitter.com/Twitter-REST-API-Method%3A-friends%C2%A0ids
        http://api.twitter.com/1/friends/ids/therm000.json 
        '''
        nodes = self.friends()
        return [], map(lambda x : (self, x), nodes)        


    def grab_user_details(self):
        '''
        detailed user info
        http://apiwiki.twitter.com/Twitter-REST-API-Method%3A-users%C2%A0show
        http://api.twitter.com/1/users/show.json?id=14704398
        '''

        if self.screen_name:
            url = 'http://api.twitter.com/1/users/show.json?screen_name=%s' % self.screen_name
        elif self.num_id:
            url = 'http://api.twitter.com/1/users/show.json?id=%d' % self.num_id
            
        json_string = urllib2.urlopen(url).read()
        
        self.user_details = json.loads(json_string)

        if self.screen_name:
            self.num_id = self.user_details['id']
        elif self.num_id:
            self.screen_name = self.user_details['screen_name']
        

class TwitterControlledNode(TwitterNode):
    
    
    def get_tenminutemail(self):
        
        mail_url = 'http://10minutemail.com/10MinuteMail/'
        self.mail_url = mail_url

        self.__br = Browser()
        #self.__br.set_proxies(proxies_per_proto)
        self.__br.set_debug_http(self.debug)
        
        # no handling of robots.txt to avoid extra GETs.
        self.__br.set_handle_robots(False)
        
        resp = self.__br.open(mail_url)        
        cont = resp.read()
        
        mail = re.findall('[a-z0-9]+@bofthew\.com', cont)[0]
        return mail
    
    
    def confirm_tenminutemail(self, mail_number=0):
        
        confirm_mail_url = 'http://10minutemail.com/10MinuteMail/index.html?dataModelSelection=message%3Aemails%5B' + str(mail_number) + '%5D&actionMethod=index.xhtml%3AmailQueue.select' 
        
        print 'Waiting 60 seconds to try confirm e-mail...'
        time.sleep(60.0)
    
        attempts = 19
        while attempts > 0:
            self.__br.open( self.mail_url )
            time.sleep(1.0)
            print 'waiting 0 ...'
            resp = self.__br.open( confirm_mail_url )
            cont = resp.read()
            print 'waiting 1...'  
            time.sleep(1.0)    
            #print cont
            print 'waiting 2...'  
            time.sleep(1.0)    
            try:
                twitter_confirm_mail_url = re.findall('http:\/\/twitter\.com\/account\/confirm_email\/[a-zA-Z0-9_-]+\/[a-zA-Z0-9_-]+', cont)[0]
                resp = self.__br.open( twitter_confirm_mail_url )
                print 'waiting 3 (good arrival of confimation mail???)...'
                time.sleep(1.0)                
                # sign in to finish!
                cont = resp.read()
                self.__br.select_form(nr=1)
                self.__br['session[username_or_email]'] = self.email
                self.__br['session[password]'] = self.passwd
                resp = self.__br.submit()                
                print 'waiting 4 (good confimation mail arrival, signing in to twitter to complete confirmation???)...'
                time.sleep(1.0)
                break
            except:
                attempts -= 1
                print 'Waiting 60 seconds to retry confirm e-mail (attempt left %d) ...' % attempts
                time.sleep(60.0)
                
                if attempts == 12:
                    resp = self.__br.open( self.mail_url )
                    cont = resp.read()
                    extend_time_url = re.findall('http:\/\/10minutemail\.com\/10MinuteMail\/index\.html\?cid=[0-9]+&actionMethod=index\.xhtml%3AmailQueue\.resetSessionLife', cont)
                    self.__br.open( extend_time_url )
                    print 'waiting (extending 10minutemail time)...'
                    time.sleep(5.0)
                
        if attempts == 0:
            raise Exception('Error: unable to confirm e-mail for Twitter!') 
            
    
    def __init__(self, complete_name=None, screen_name=None, passwd=None, create=True):
        '''
        Constructor
        '''
        
        self.debug = True
        
        if not screen_name or not complete_name or not passwd:            
            raise Exception('no Twitter screen name or no complete name or no passwd specified specified!')
        
        self.complete_name = complete_name
        self.screen_name = screen_name
        self.passwd = passwd
        self.email = self.get_tenminutemail() #'thisisthecanary2@spamex.com' # 'a2291229@bofthew.com'  #screen_name + '.1.thisisthecanary@spamgourmet.com'
        print self.email

        if not create:
            self.__settings = twython.setup(
                                            username=self.screen_name,
                                            password=self.passwd,
                                            )            
            return
        
        #self.__br = Browser()
        #self.__br.set_proxies(proxies_per_proto)
        #self.__br.set_debug_http(True)
        
        # no handling of robots.txt to avoid extra GETs.
        #self.__br.set_handle_robots(False)

        try:
            # sign into Twitter
            resp = self.__br.open("https://twitter.com/signup")
            
            cont = resp.read()
            recaptcha_url = re.findall('https:\/\/api-secure.recaptcha.net\/challenge\?k=[a-zA-Z0-9]+',  cont)[0]
            
            recaptcha_cont = urllib2.urlopen(recaptcha_url).read()
            print recaptcha_cont
            recaptcha_challenge = re.findall('challenge : \'[a-zA-Z0-9_-]+\'', recaptcha_cont)[0][len('challenge : \''):-len('\'')]
            
            print 'opening https://api-secure.recaptcha.net/image?c=%s' % recaptcha_challenge
            recaptcha_jpg = urllib2.urlopen('https://api-secure.recaptcha.net/image?c=%s' % recaptcha_challenge).read()
            
            jpg_filename = '/tmp/%s.jpg' % time.ctime().replace(' ','_')
            jpg = open(jpg_filename, 'w')
            jpg.write(recaptcha_jpg)
            jpg.close()
            os.system('eog %s' % jpg_filename)
    
            recaptcha_response = raw_input("Enter recaptcha words: ")
    
            url = 'https://twitter.com/account/create'
            values = {'user[name]' : complete_name,
                      'user[screen_name]' : screen_name,                  
                      'user[user_password]' : passwd,
                      'user[email]' : self.email,
                      'recaptcha_response_field' : recaptcha_response,
                      'recaptcha_challenge_field' : recaptcha_challenge
                       }
    
            data = urllib.urlencode(values)
            req = urllib2.Request(url, data)
    
            self.__br.select_form(nr=0)
            resp = urllib2.urlopen(req)
    
            time.sleep(2.0)
                
            self.__good = True

            #json_string = self.__br.open(self.user_url % self.screen_name).read() 
            #user_profile = json.loads(json_string)
            #self.user_details = user_profile
            #self.num_id = user_profile['id']
            
        except Exception, e:
            print str(e)    
            print 'EXCEPTION on TwitterControlledNode, possibly bad user/password or https login don\' work behind a proxy.'
            self.__good = False
            
        if self.__good:
            
            self.confirm_tenminutemail()
            
            self.__settings = twython.setup(
                                            username=self.screen_name,
                                            password=self.passwd,
                                            )            
        
        
    def __confirm_email(self):
        
        time.sleep(5.0)
        
        

    def set_profile_image_url(self, image_local_file):
                
        self.__settings.updateProfileImage(image_local_file)

        
    def set_profile_background_image_url(self, image_local_file, tile=True):
        
        tile = tile and 'true' or 'false' 
        
        self.__settings.twythonControl.updateProfileBackgroundImage(image_local_file, tile)


    def set_profile_attribute(self, attr, value):
        '''
        Possible attributes: complete_name, email, url, location, description
        '''
        dictionary = {attr:value,}
        try:
            self.__settings.updateProfile(**dictionary)
        except:
            pass

        
    def __setattr__(self, attr, value):
        
        if attr in ['name', 'email', 'url', 'location', 'description']:
            self.set_profile_attribute(attr, value)        

        if attr in [
                    'profile_background_color',
                    'profile_text_color',
                    'profile_link_color',
                    'profile_sidebar_fill_color',
                    'profile_sidebar_border_color'                    
                    ]:
            self.set_profile_colors(attr, value)
        
        object.__setattr__(self, attr, value)
                

    def set_profile_colors(self, attr, value):
        '''
        Colorizable thins:            'profile_background_color',
                                      'profile_text_color',
                                      'profile_link_color',
                                      'profile_sidebar_fill_color',
                                      'profile_sidebar_border_color'

        '''
        dictionary = {attr:value,}
        self.__settings.updateProfileColors(**dictionary)

    
    def set_status(self, status):
        
        if len(status) > 140:
            raise TwitterNodeException('ERROR: status too long!!')
        
        self.__settings.updateStatus(status)    

        
        

class TwitterFriendVisitor(Visitor):

    def setTwitterBrowser(self, tw_browser):
        
        self.twitter_browser = tw_browser


    def visitTwitterNode(self, node, *args):
        
        print 'Visitando nodo twitter: id = %s, user = %s' % (node.num_id, node.screen_name) 
    
        tw_local_graph = Graph()
        
        friends = self.twitter_browser.friends(node)
        for f in friends:
            tw_local_graph.add_edge(node, f)
            
        return tw_local_graph
        
        
 
if __name__ == '__main__':
    
    possible_passwd = base64.b64encode(str(random.random()))[3:18].lower()
    
    screen_name = base64.b64encode(str(random.random()))[1:13].lower()
    #screen_name = 'mc40mdcx'
    passwd = 'asdfasdf'
    print screen_name
    node = TwitterControlledNode(screen_name, screen_name, 'asdfasdf', create=True)
    
    #print node.get_tenminutemail()
    
    #node.set_profile_image_url('/data/fotos/arte_seleccion/atlantes_chica.jpg')
    

