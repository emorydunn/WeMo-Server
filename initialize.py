#!/usr/bin/env python

import os, re, time, sys
from ouimeaux.environment import Environment
os.system('clear')

def on_switch(switch):
    print "Switch found!", switch.name
    #pass

env = Environment(on_switch)

env.start()

env.discover(seconds=15)

env.list_switches()

