#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep
import cgi
import os, urlparse
from ouimeaux.environment import Environment
from static import static

os.system('clear')
#import web_auth

PORT_NUMBER = 9090
exist = None

def on_switch(switch):
    print "Switch found!", switch.name
    pass


#status_html = "<head><title>Switch Status</title></head><h2>Switches from alias list:</h2>"


#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):
    
    #Handler for the GET requests
    def do_GET(self):
        #print(self.path)
        if self.path=="/":
            self.path="/index.html"
        if self.path == '/status':
            self.path = '/status.html'
        if self.path == '/status/':
            self.path = '/status.html'

            

        try:
            #Check the file extension required and
            #set the right mime type

            sendReply = False
            switches = False
            mimetype='text/html'
            if self.path.endswith(".html"):
                mimetype='text/html'
                sendReply = True
            if self.path.endswith(".jpg"):
                mimetype='image/jpg'
                sendReply = True
            if self.path.endswith(".png"):
                mimetype='image/png'
                sendReply = True
            if self.path.endswith(".gif"):
                mimetype='image/gif'
                sendReply = True
            if self.path.endswith(".js"):
                mimetype='application/javascript'
                sendReply = True
            if self.path.endswith(".css"):
                mimetype='text/css'
                sendReply = True
                
            parsed_path = urlparse.urlparse(self.path.replace('/', ''))
            #print parsed_path
            try:
                params = dict([p.split('=') for p in parsed_path[4].split('&')])
                switches = True
                sendReply = False
            except:
                params = {}
        

            if switches == True:
                self.send_response(200)
                self.send_header('Content-type',mimetype)
                self.end_headers()
                print ("State changes:")
                for key in params:
                    self.name = wemo.get(key, None)
                    if self.name:
                        #print self.name, params[key]
                        if params[key] == "on":
                            state = 1
                            #print state
                        if params[key] == "off":
                            state = 0
                            #print state
                        try:
                            switch = env.get_switch(self.name)
                            switch.basicevent.SetBinaryState(BinaryState=state)
                            if switch.get_state() == 0:
                                print ' -'+self.name,'is off.'
                                self.stateH = 'off'
                                self.wfile.write("<head><title>Switch Status</title></head>")
                                #self.wfile.write("<head><title>"+self.name+": " +self.stateH+ "</title></head>")
                                self.wfile.write(self.name+ " is currently " +self.stateH+ ". <br>")
                            else:
                        		#switch.get_state() == 1:
                                print ' -'+self.name,'is on.'
                                self.stateH = 'on'
                                self.wfile.write("<head><title>Switch Status</title></head>")
                                #self.wfile.write("<head><title>"+self.name+": " +self.stateH+ "</title></head>")
                                self.wfile.write(self.name+ " is currently " +self.stateH+ ". <br> ")
                        except: 
                            print (' -'+self.name+ " doesn't exist.")
                            self.wfile.write("<head><title>Switch Status</title></head>")
                            #self.wfile.write("<head><title>"+self.name+": missing </title></head>")
                            self.wfile.write(self.name+ " doesn't exist.<br>")
                            pass
            
            if sendReply == True:
                '''print self.path
                self.first, self.colon, self.rest = self.path.partition('?')
                print self.first'''
                #Open the static file requested and send it
                self.send_response(200)
                self.send_header('Content-type',mimetype)
                self.end_headers()
                try:
                    self.wfile.write(self.name+ " is currently " +self.stateH+ ". ")
                except: #The Status Board
                    if self.path == '/status.html':
                       
                        status_html = open('status.html', 'r')
                        content = status_html.read()
                        print content
                        self.wfile.write(content)
                        
                        print ("Switches from alias list:")
                        '''self.wfile.write("<head><title>Switch Status</title></head>")
                        self.wfile.write("<h2>Switches from alias list:</h2>")'''
                        
                        for key in wemo:
                            self.name = wemo.get(key, None)
                            #print self.name
                            try:
                                switch = env.get_switch(self.name)
                                #print switch
                                if switch.get_state() == 0:
                                    print ' -'+self.name,'is off.'
                                    self.stateH = 'off'
                                    self.wfile.write("<div id=status>" +self.name+ " is currently " +self.stateH+ ". <img src='img/forward.png'></div> <br>")
                                else:
                            		#switch.get_state() == 1:
                                    print ' -'+self.name,'is on.'
                                    self.stateH = 'on'
                                    self.wfile.write("<div id=status>" +self.name+ " is currently " +self.stateH+ ". <img src='img/forward.png'></div> <br>")
                            except:
                                print (' -'+self.name+ " doesn't exist.")
                                self.wfile.write("<div id=status>" +wemo[key]+ " doesn't exist.<br></div>")
                    else:
                        f = open(curdir + sep + self.path) 
                        self.wfile.write(f.read())
                        f.close()
            
            return

        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)

    #Handler for the POST requests
    def do_POST(self):
        pass
        
class aliases(): #Load the shortcuts into a dict
    def __init__(self):
        with open(os.path.abspath("/Users/emorydunn/.wemo/config.yml")) as a:
            for line in a.readlines():
                #print line
                if line.startswith('    '):
                    #print line[:-1]
                    
                    first, colon, rest = line.partition(':')
                    first = first[4:]
                    rest = rest[1:-1]
                    #print (first, colon, rest)
                    
                    wemo[first] = rest
                    assert wemo[first] == rest


env = Environment(on_switch)
env.discover(seconds=3)
env.start()
wemo = {}
aliases()
#oh = env.get_switch('Office Heater')


try:
    #Create a web server and define the handler to manage the
    #incoming request
    server = HTTPServer(('', PORT_NUMBER), myHandler)
    print 'Started httpserver on port ' , PORT_NUMBER
    
    #Wait forever for incoming htto requests
    server.serve_forever()

except KeyboardInterrupt:
    print '^C received, shutting down the web server'
    server.socket.close()
