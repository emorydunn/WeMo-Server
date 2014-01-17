class static():
    def status(self, name, stateH):
        print ("Switches from alias list.")
        self.wfile.write("<h2>Switches from alias list:</h2>")
        
        for key in wemo:
            self.name = wemo.get(key, None)
            #print self.name
            try:
                switch = env.get_switch(self.name)
                #print switch
                if switch.get_state() == 0:
                    print self.name,'is off.'
                    self.stateH = 'off'
                    self.wfile.write(self.name+ " is currently " +self.stateH+ ". <br>")
                else:
            		#switch.get_state() == 1:
                    print self.name,'is on.'
                    self.stateH = 'on'
                    self.wfile.write(self.name+ " is currently " +self.stateH+ ". <br> ")
            except:
                print (self.name+ " doesn't exist.")
                self.wfile.write(wemo[key]+ " doesn't exist.<br>")