#Version: 0.6 BETA
#Author: Emory Dunn

# TODO Set cookie after accepting yubikey. Set a timer instead. 
# TODO Associate switches with users
# TODO If a switch goes offline have a reasonable timeout for loading the page. 

#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep
import cgi
import os, urlparse, time
from ouimeaux.environment import Environment
from static import static
import csv, decrypt

os.system('clear')
#import web_auth

PORT_NUMBER = 9090
exist = None
accepted =  False
loginTime = False

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
                timer()
                if accepted == True:  
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
                else: 
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
                
                #The Status Board
                if self.path == '/status.html':
                    #print ("sendReply")
                    timer()
                    if accepted == True: 
                        status_html = open('status.html', 'r')
                        page = status_html.read()
                        #print content
                        self.wfile.write(page)
                
                        self.wfile.write("<div id=status>\n")
                        self.wfile.write("<table>\n")
                
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
                        
                                self.wfile.write("\n<tr>\n")
                                self.wfile.write("<td>"+self.name+ " is currently " +self.stateH+ ".</td>")
                                self.wfile.write("<td><a href='status?"+key+"="+self.stateHi+"'><img src='img/forward.png'></a></td>")
                                self.wfile.write("\n</tr>\n")
                            except:
                                print (' -'+self.name+ " doesn't exist.")
                                self.wfile.write("\n<tr>\n")
                                self.wfile.write("<td>"+wemo[key]+ " doesn't exist.</td>")
                                self.wfile.write("\n</tr>\n")
                    
                        self.wfile.write("</table>\n")
                        
                        self.wfile.write("\n</div>")
                
                        self.wfile.write("\n\n</body>\n</html>")
                        
                    else: 
                        f = open(curdir + sep + "index.html")
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
            if self.path == '/status':
                ##################### Yubikey
                form = cgi.FieldStorage(
                    fp=self.rfile, 
                    headers=self.headers,
                    environ={'REQUEST_METHOD':'POST',
                        'CONTENT_TYPE':self.headers['Content-Type'],
                })
                otp = form["password"].value
                print "Your OTP is: %s" % form["password"].value
                self.send_response(200)
                self.end_headers()
        #			self.wfile.write("Thanks %s !" % form["password"].value)


        #Extract Public Key
                public = otp[:12]
        #Check OTP
                with open('otp.log', 'rb') as log:
                    reader = csv.reader(log)
                    for row in reader:
                        col1 = row
                        if otp in row:
                            key = ("true")
                        else:
                            key = ("false")

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
                            exist = ("true")


                            if key == ("true"):
                                print("Key already used.")
                                self.wfile.write("Key already used.")
                            elif exist == None:
                                print("User not found.")
                                self.wfile.write("User not found")
                            else:
                                yubikey = decrypt.YubikeyToken(otp, aes_key)
                                if yubikey.crc_ok:
                                    if  yubikey.secret_id == priv:
                                        print("Welcome, {}.".format(name))
                                        #self.wfile.write("Welcome, {}.".format(name))
                                        #self.path = "/status.html"
                                        global loginTime
                                        loginTime = (round(int(time.time()), 10))
                                        print loginTime
                                        
                                else:
                                    print("Key not valid.")
                                    self.wfile.write("Key not valid.")
                
                #####################
                timer()
                if accepted == True: 
                    #print ("POST")
                    status_html = open('status.html', 'r')
                    page = status_html.read()
                    #print content
                    self.wfile.write(page)
                
                    self.wfile.write("<div id=status>\n")
                    self.wfile.write("<table>\n")
                
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
                        
                            self.wfile.write("\n<tr>\n")
                            self.wfile.write("<td>"+self.name+ " is currently " +self.stateH+ ".</td>")
                            self.wfile.write("<td><a href='status?"+key+"="+self.stateHi+"'><img src='img/forward.png'></a></td>")
                            self.wfile.write("\n</tr>\n")
                        except:
                            print (' -'+self.name+ " doesn't exist.")
                            self.wfile.write("\n<tr>\n")
                            self.wfile.write("<td>"+wemo[key]+ " doesn't exist.</td>")
                            self.wfile.write("\n</tr>\n")
                    
                    self.wfile.write("</table>\n")
                        
                    self.wfile.write("\n</div>")
                
                    self.wfile.write("\n\n</body>\n</html>")
        
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
