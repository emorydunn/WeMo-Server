#!/usr/bin/env python

import os, re, time, sys
from ouimeaux.environment import Environment
os.system('clear')

def on_switch(switch):
	#print "Switch found!", switch.name
    pass

def toggle():
    '''Turn the switch on if off and off if on. '''
    if switch.get_state() == 0:
		switch.on()
		print('Turning ' +switch_name+ ' on.')
    else:
		#switch.get_state() == 1:
		switch.off()
		print('Turning ' +switch_name+ ' off.')

class get_time():
    '''Search for numbers in the input string'''
    def __init__(self, text):
        #print('get_time: ' +text)
        
        try:
            self.t = int(re.search(r'\d+', text).group())
        except:
            self.t = int(0)
        
        #print(self.t) #Debug

class interval():
    '''Get the time interval of time from the string'''
    def __init__(self, text):
        try:
            self.s = re.search('seconds', text).group()
            #print(self.s) #Debug
            self.type = ('seconds')
        except:
            try:
                self.m = re.search('minutes', text).group()
                #print(self.m) #Debug
                self.type = ('minutes')
            except:
                try:
                    self.h = re.search('hours', text).group()
                    #print(self.h) #Debug
                    self.type = ('hours')
                except:
                    try:
                        self.h = re.search('hour', text).group()
                        #print(self.h) #Debug
                        self.type = ('hour')
                    except:
                        self.type = None

env = Environment(on_switch)

env.start()

'''Show all the WeMo searching stuff'''
# env.discover(seconds=3)

switch = env.get_switch('Office Heater')
switch_name = 'Office Heater'

total = len(sys.argv)
#print(total)
flip = None

if total == 2:
    if str(sys.argv[1]) == ('on'):
        answer = ('on')
        flip = True
    if str(sys.argv[1]) == ('off'):
        answer = ('off')
        flip = True
elif not total == 4:
    if switch.get_state() == 0:
    	print(switch_name+ ' is off. Would you like to turn it on, for how long?')
    else:
    	print(switch_name+ ' is on. Would you like to turn it off, for how long?')
    answer = raw_input('>>> ')
else:
    answer = str(sys.argv[1]) + str(sys.argv[2]) + str(sys.argv[3])
    #print(total) #Debug
    #print(answer) #Debug

'''Set the interval multiplier'''
interval = interval(answer)
if interval.type == ('seconds'):
    #print('seconds') #Debug
    multiplier = 1
elif interval.type == ('minutes'):
    #print('minutes') #Debug
    multiplier = 60
elif interval.type == ('hours'):
    #print('minutes') #Debug
    multiplier = 3600
elif interval.type == ('hour'):
    #print('minutes') #Debug
    multiplier = 3600
else:
    multiplier = 1

'''
Debug
print(timer.t)'''


timer = get_time(answer)
current_time = (round(int(time.time()), 10))
minutes = timer.t * multiplier
timeout = current_time + minutes


#Debug
'''print(current_time)
print(minutes)
print(timeout)'''


'''Parse the initial word'''
if answer.startswith('yes') == True:
    toggle()
    if not timer.t == 0:
        #print(interval.type) #Debug
        print('Waiting for ' +str(timer.t)+ ' ' +str(interval.type)+ '.')
elif answer.startswith('no') == True:
	if switch.get_state() == 0:
		print('Leaving ' +switch_name+ ' off.')
	else:
		print('Leaving ' +switch_name+ ' on.')
elif answer.startswith('on') == True:
    #print (switch.get_state()) #Debug
    if not switch.get_state() == 1:
        print('Turing ' +switch_name+ ' on.')
    else:
        print('Leaving ' +switch_name+ ' on.')
        minutes = 0
    switch.on()
elif answer.startswith('off') == True:
    #print (switch.get_state()) #Debug
    if not switch.get_state() == 0:
        print('Turing ' +switch_name+ ' off.')
    else:
        print('Leaving ' +switch_name+ ' off.')
        minutes = 0
    switch.off()
else:
    print('Not doing anything. ')

'''The timeout clock'''
if not minutes == 0:
    while current_time < timeout:
        
        '''
        Debug
        print(current_time)
        print(timeout)
        print(timeout - current_time)
        '''
        current_time = (round(int(time.time()), 10))
        time.sleep(1)
    if flip == None:
        toggle()