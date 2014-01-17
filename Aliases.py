import os, urlparse
from ouimeaux.environment import Environment
#print config

def on_switch(switch):
    print "Switch found!", switch.name
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
                        
class linereader():
    def __init__(self):
        parsed_path = urlparse.urlparse(URL.replace('/', ''))
        try:
            self.params = dict([p.split('=') for p in parsed_path[4].split('&')])
        except:
            self.params = {}
            
            
os.system('clear')
env = Environment(on_switch)
#env.discover(seconds=3)
env.start()

wemo = {}
short = aliases()

print wemo

URL = '/?oh=on&lamp=off/'
#URL = '/?oh=off'
parse = linereader()
print parse.params

for key in parse.params:
    name = wemo.get(key, None)
    if name:
        print name, parse.params[key]
        if parse.params[key] == "on":
            state = 1
            print state
        if parse.params[key] == "off":
            state = 0
            print state
        try:
            switch = env.get_switch(name)
            switch.basicevent.SetBinaryState(BinaryState=state)
        except: 
            print ("Doesn't exist.")
            pass

#print short.string

#string = "    oh: Office Heater"
