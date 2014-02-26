#Version: 0.6 BETA 5
#Author: Emory Dunn

# TODO Set cookie after accepting yubikey. 
#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep
import cgi
import os, urlparse, time
from ouimeaux.environment import Environment
from static import static
import csv
from yubikey import decrypt
import Cookie, requests

os.system('clear')
#import web_auth

PORT_NUMBER = 9090
exist = None
#accepted =  False
#global loginTime
#loginTime = False


def on_switch(switch):
    print "Switch found!", switch.name
    pass

#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):
    
    #Handler for the GET requests
    def do_GET(self):
        #print(self.path)
        # TODO Make any path not ending in an extension redirect to an HTML page. 
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
            '''if self.path.endswith("/"):
                print self.path
                mimetype='text/html'
                sendReply = True
                self.path = self.path[:-1]+ ".html"
                print self.path'''
                
            parsed_path = urlparse.urlparse(self.path.replace('/', ''))
            #print parsed_path
            #print 'Parsed_path: ' +parsed_path[2]
            
            #If there are params on the URL check what needs to be done
            try:
                params = dict([p.split('=') for p in parsed_path[4].split('&')])
                
                #If params are on a URL that shouldn't accept them
                if parsed_path[2] == (''):
                    self.path = 'index.html'
                    sendReply = True
                elif parsed_path[2].endswith('.html'):
                    self.path = parsed_path[2]
                    sendReply = True
                    #print 'Path: ' +self.path
                else: 
                    self.path = parsed_path[2]+ '.html'
                    sendReply = True
                    #print 'Path: ' +self.path
                    
                #Match the path of a POST request to redirect to the status page.
                login.get()
                if login.accepted == True:  #Check if the login is valid, if so allow POST to run. 
                    if parsed_path[2] == 'status': 
                        self.path = '/status.html'
                        switches = True
                        sendReply = True
                        print ('Status match')
                    elif parsed_path[2] == 'status.html':
                        self.path = '/status.html'
                        switches = True
                        sendReply = True
                        print ('Status match')
                else: #If not, continue to show the page, but don't parse POST
                    print ("accepted == False")
                    if parsed_path[2] == 'status': 
                        self.path = '/status.html'
                        switches = False
                        sendReply = True
                        print ('Status match')
                    elif parsed_path[2] == 'status.html':
                        self.path = '/status.html'
                        switches = False
                        sendReply = True
                        print ('Status match')
                    
            except:
                params = {}
        

            if switches == True:
                print ("State changes:")
                for key in params:
                    self.name = wemo.get(key, None)
                    if self.name:
                        print self.name, params[key]
                        #If the paremter isn't on or off the state doesn't change. 
                        if params[key] == "on":
                            state = 1
                            #print state
                        if params[key] == "off":
                            state = 0
                            #print state
                        try:
                            #Set the state of the switch and print the result
                            switch = env.get_switch(self.name)
                            switch.basicevent.SetBinaryState(BinaryState=state)
                            
                            print ' -'+self.name+' is ' +params[key]+'.'
                            
#                           "" if switch.get_state() == 0:
#                                print ' -'+self.name,'is off.'
#                            else:
#                        		#switch.get_state() == 1:
#                                print ' -'+self.name,'is on.'""
                        except: 
                            print (' -'+self.name+ " doesn't exist.")
                            pass
            
            if sendReply == True:
                #Open the static file requested and send it
                self.send_response(200)
                self.send_header('Content-type',mimetype)
                self.end_headers()
                
                
                ##################### Status Page
                #The Status Board
                if self.path == '/status.html':
                   #print ("sendReply")
                    #login.get()
                    
                    login.get()
                    
                    if login.accepted == True: #If the login is valid, show the status page. 
                        #status_html = open('status.html', 'r')
                        #page = status_html.read()
                        #print content
                        #self.wfile.write(page)
                        
                        self.wfile.write("<html>\n<body>\n")
                        self.wfile.write("<div id='title'><h2>Switches:</h2></div>\n")
                        self.wfile.write("\n<div id=status>\n")
                        #self.wfile.write("<table>\n")
                
                        print ("Switches from alias list:")
                
                        for key in wemo:
                            self.name = wemo.get(key, None)
                    
                            #print self.name
                            try:
                                switch = env.get_switch(self.name)
                                #print switch
                                print ("Checking state")
                                if switch.get_state() == 0: #Set boolean states
                                    self.stateH = 'off'
                                    self.stateHi = 'on'
                                    #print ("State 0")
                                elif switch.get_state() == 1:
                                    self.stateH = 'on'
                                    self.stateHi = 'off'
                                    #print ("State 0")
                                else:
                                    print ("Bad State. ")
                                    pass
                        
                                print (' -'+self.name+' is '+self.stateH+'.')
                        
                                #self.wfile.write("\n<tr>\n")
                                #self.wfile.write("<td>"+self.name+ " is currently " +self.stateH+ ".</td>")
                                #self.wfile.write("<td><a href='status?"+key+"="+self.stateHi+"'><img src='img/forward.png'></a></td>")
                                #self.wfile.write("\n</tr>\n")
                                
                                self.wfile.write(self.name+ " is currently " +self.stateH+ ".\n")
                                self.wfile.write("<a href='status?"+key+"="+self.stateHi+"'><img src='img/forward.png'></a><br>\n")
                            except:
                                print (' -'+self.name+ " doesn't exist.")
                                #self.wfile.write("\n<tr>\n")
                                #self.wfile.write("<td>"+wemo[key]+ " doesn't exist.</td>")
                                #self.wfile.write("\n</tr>\n")
                                
                                
                                self.wfile.write(wemo[key]+ " doesn't exist.<br>\n")
                                
                    
                        #self.wfile.write("</table>\n")
                        
                        self.wfile.write("\n</div>")
                
                        #self.wfile.write("\n\n</body>\n</html>")
                        
                    else: #If not, redirect to the index page. 
                        f = open(curdir + sep + "index.html")
                        #print "Other: " +self.path
                        self.wfile.write(f.read())
                        f.close()
                        
                    ##################### End Status Page
                    
                if self.path == '/index.html':
                   #print ("sendReply")
                    login.get()
                    if login.accepted == True: #If the login is valid, redirect to status page.
                        self.wfile.write('<html><head><meta http-equiv="refresh" content="0; url=/status.html" /></head></html>')
                    else:
                        f = open(curdir + sep + self.path)
                        #print "Other: " +self.path
                        self.wfile.write(f.read())
                        f.close()
                
                else:
                    f = open(curdir + sep + self.path)
                    #print "Other: " +self.path
                    self.wfile.write(f.read())
                    f.close()
            
            return

        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)

    #Handler for the POST requests
    def do_POST(self):
            if self.path == '/login':
                bypass = False
                ##################### Yubikey
                try:
                    form = cgi.FieldStorage(
                        fp=self.rfile, 
                        headers=self.headers,
                        environ={'REQUEST_METHOD':'POST',
                            'CONTENT_TYPE':self.headers['Content-Type'],
                    })
                    otp = form["password"].value
                    print "Your OTP is: %s" % form["password"].value
                    #self.send_response(200)
                    #self.end_headers()
        #			self.wfile.write("Thanks %s !" % form["password"].value)
                except:
                    print ("No password")
                    otp = None


                if not otp == None:
            #Extract Public Key
                    public = otp[:12]
            #Check OTP
                    with open('otp.log', 'rb') as log:
                        reader = csv.reader(log)
                        for row in reader:
                            col1 = row
                            if otp in row:
                                key = True
                            else:
                                key = False
                            #print (key)

            #Log OTP
                    with open('otp.log', 'a') as log:
                        auth_write = csv.writer(log)
                        auth_write.writerow([otp])

            #Set Variables

                    with open('auth.csv', 'rb') as f:
                        reader = csv.reader(f)
                        for row in reader:
                            col1, col2, col3, col4, col5 = row
                            if public in row:
                                pub = col2
                                priv = col3
                                aes_key = col4
                                name = col5
                                #print pub, name
                                exist = True
                            elif public == "valid":
                                bypass = True
                            else:
                                exist = None

                #global loginTime
                if bypass == True:
                    global loginTime
                    loginTime = (round(int(time.time()), 10))
                    print loginTime
                elif otp == None:
                    status_html = open('status.html', 'r')
                    page = status_html.read()
                    #print content
                    self.wfile.write(page)
                    self.wfile.write("<div id='title'><h2>Login Error</h2></div>")
                    
                    print("User not found.")
                    self.wfile.write("<div id=status>\nNo key was input. \n</div>")
                    # TODO Message not showing. 
                    loginTime = False
                elif key == True:
                    
                    status_html = open('status.html', 'r')
                    page = status_html.read()
                    #print content
                    self.wfile.write(page)
                    self.wfile.write("<div id='title'><h2>Login Error</h2></div>")
                    
                    print("Key already used.")
                    self.wfile.write("<div id=status>\nKey already used.\n</div>")
                    loginTime = False
                elif exist == True:
                    yubikey = decrypt.YubikeyToken(otp, aes_key)
                    if yubikey.crc_ok:
                        if yubikey.secret_id == priv:
                            print("Welcome, {}.".format(name))
                            #global loginTime
                            #loginTime = (round(int(time.time()), 10))
                            #print loginTime
                            #login = cookie()
                            loginName = ("{}".format(pub))
                            login.set(loginName)
                            #print ("Good" +login.ch)
                            self.send_response(200)
                            self.send_header('Set-Cookie', login.ch)
                            self.send_header('Content-type', "text/html")
                            self.end_headers()
                            
                    else:
                        
                        status_html = open('status.html', 'r')
                        page = status_html.read()
                        #print content
                        self.wfile.write(page)
                        self.wfile.write("<div id='title'><h2>Login Error</h2></div>")
                        
                        print("Key not valid.")
                        self.wfile.write("<div id=status>\nKey not valid. \n</div>")
                        loginTime = False
                elif exist == None: # exist == None:
                    
                    status_html = open('status.html', 'r')
                    page = status_html.read()
                    #print content
                    self.wfile.write(page)
                    self.wfile.write("<div id='title'><h2>Login Error</h2></div>")
                    
                    print("User not found.")
                    self.wfile.write("<div id=status>\nUser not found. \n</div>")
                    # TODO Message not showing. 
                    loginTime = False
                ##################### End YubiKey
                
                print "Calling get"
                try:
                    
                    
                    #self.send_response(200)
                    #self.send_header('Cookie', 'login=hi')
                    #self.read_header('Content-type', "text/html")
                    #self.end_headers()
                    
                    
                    
                    login.get()
                    
                    print ("Got")
                except:
                    print ("Failed")
                print login.accepted
                if login.accepted == True: #Redirect to Status Page
                    print ("True")
                    self.wfile.write('\n\n<html><head><meta http-equiv="refresh" content="0; url=/status.html" /></head></html>')
                    
            if self.path == '/':
                #Logout
                form = cgi.FieldStorage(
                    fp=self.rfile, 
                    headers=self.headers,
                    environ={'REQUEST_METHOD':'POST',
                        'CONTENT_TYPE':self.headers['Content-Type'],
                })
                loginTime = False
                login.expired()
                print ("Logging out. ")
                
                self.send_response(200)
                self.send_header('Set-Cookie', login.cl)
                self.send_header('Content-type', "text/html")
                self.end_headers()
                
                f = open(curdir + sep + "index.html")
                #print "Other: " +self.path
                self.wfile.write(f.read())
                f.close()
                
            if self.path == '/settings.html':
                #Refresh Aliases
                form = cgi.FieldStorage(
                    fp=self.rfile, 
                    headers=self.headers,
                    environ={'REQUEST_METHOD':'POST',
                        'CONTENT_TYPE':self.headers['Content-Type'],
                })
                aliases()
                self.send_response(200)
                self.end_headers()
                f = open(curdir + sep + "settings.html")
                #print "Other: " +self.path
                self.wfile.write(f.read())
                f.close()
        
class aliases(): #Load the shortcuts into a dict
    def __init__(self):
        global wemo
        wemo = {}
        print ("Refreshing alias list: ")
        with open(os.path.abspath("/Users/emorydunn/.wemo/config.yml")) as a:
            for line in a.readlines():
                #print line
                if line.startswith('    #'):
                    pass
                elif line.startswith('    '):
                    #print line[:-1]
                    
                    first, colon, rest = line.partition(':')
                    first = first[4:]
                    rest = rest[1:-1]
                    print ('    ' +first+ ': ' +rest)
                    
                    wemo[first] = rest
        #print wemo
                    #assert wemo[first] == rest

#Timer called anytime the validity of the login needs to be checked. 
#loginTime set when a valid key is input. 
class timer():
    def __init__(self):
        global accepted
        global loginTime
        #print loginTime
        timeout = 3600
        logoutTime = loginTime + timeout
        #print logoutTime
        #print (round(int(time.time()), 10))
        if loginTime == False:
            accepted = False
        elif time.time() < logoutTime:
            accepted = True
        else:
            accepted = False

class cookie():
    """docstring for cookie"""
    def set(self, loginName):
        print loginName
        self.c = Cookie.SimpleCookie()
    
        self.c['login'] = loginName
        self.c['login']['expires'] = 1*1*3*60*60
    
        print (self.c)
        self.ch = self.c.output(header='')
        
        #opener = urllib2.Request('http://emorys-macbook-pro.local:9090')
        #opener.add_headers.append(('Set-Cookie', self.c))
        
    def get(self):
        """docstring for get"""
        print ("Get")
        
        if 'HTTP_COOKIE' in os.environ:
            print ("Cookies!")
            cookie_string=os.environ.get('HTTP_COOKIE')
            cr=Cookie.SimpleCookie()
            cr.load(cookie_string)

            try:
                data=cr['login'].value
                print "cookie data: "+data+"<br>"
                self.accepted = True
            except KeyError:
                print "The cookie was not set or has expired<br>"
                self.accepted = False
        #else:
            #print ("The mouse ate the cookies")
            #self.accepted = False
            
    def expired(self):
        """docstring for expired"""
        print ("Logging Out")
        #print loginName
        c = Cookie.SimpleCookie()
    
        c['login'] = ''
        c['login']['expires'] = 'Thu, 01 Jan 1970 00:00:00 GMT'
    
        print (c)
        self.cl = c.output(header='')
                  


env = Environment(on_switch)
env.discover(seconds=3)
env.start()
aliases()
login = cookie()
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
