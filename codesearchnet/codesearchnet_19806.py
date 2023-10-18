def setsweep(self, sweep=0, channel=0):
        """set the sweep and channel of an ABF. Both start at 0."""
        try:
            sweep=int(sweep)
        except:
            self.log.error("trying to set sweep to [%s]",sweep)
            return
        if sweep<0:
            sweep=self.sweeps-1-sweep # if negative, start from the end
        sweep=max(0,min(sweep,self.sweeps-1)) # correct for out of range sweeps
        if 'sweep' in dir(self) and self.sweep == sweep and self.derivative is False:
            self.log.debug("sweep %d already set",sweep)
            return
        #self.log.debug("loading sweep %d (Ch%d)",sweep,channel)
        self.channels=self.ABFblock.segments[sweep].size["analogsignals"]
        if self.channels>1 and sweep==0:
            self.log.info("WARNING: multichannel not yet supported!") #TODO:
        self.trace = self.ABFblock.segments[sweep].analogsignals[channel]
        self.sweep=sweep # currently selected sweep
        self.channel=channel # currently selected channel

        # sweep information
        self.rate = int(self.trace.sampling_rate) # Hz
        self.period = float(1/self.rate) # seconds (inverse of sample rate)
        self.pointsPerSec = int(self.rate) # for easy access
        self.pointsPerMs = int(self.rate/1000.0) # for easy access
        self.sweepSize = len(self.trace) # number of data points per sweep
        self.sweepInterval = self.trace.duration.magnitude # sweep interval (seconds)
        self.sweepLength = float(self.trace.t_stop-self.trace.t_start) # in seconds
        self.length = self.sweepLength*self.sweeps # length (sec) of total recording
        self.lengthMinutes = self.length/60.0 # length (minutes) of total recording

        if str(self.trace.dimensionality) == 'pA':
            self.units,self.units2="pA","clamp current (pA)"
            self.unitsD,self.unitsD2="pA/ms","current velocity (pA/ms)"
            self.protoUnits,self.protoUnits2="mV","command voltage (mV)"
        elif str(self.trace.dimensionality) == 'mV':
            self.units,self.units2="mV","membrane potential (mV)"
            self.unitsD,self.unitsD2="V/s","potential velocity (V/s)"
            self.protoUnits,self.protoUnits2="pA","command current (pA)"
        else:
            self.units,self.units2="?","unknown units"
            self.unitsD,self.unitsD2="?","unknown units"

        # sweep data
        self.sweepY = self.trace.magnitude # sweep data (mV or pA)
        self.sweepT = self.trace.times.magnitude # actual sweep times (sec)
        self.sweepStart = float(self.trace.t_start) # time start of sweep (sec)
        self.sweepX2 = self.sweepT-self.trace.t_start.magnitude # sweeps overlap
        self.sweepX = self.sweepX2+sweep*self.sweepInterval # assume no gaps
        if self.derivative:
            self.log.debug("taking derivative")
            #self.sweepD=np.diff(self.sweepY) # take derivative
            self.sweepD=self.sweepY[1:]-self.sweepY[:-1] # better?
            self.sweepD=np.insert(self.sweepD,0,self.sweepD[0]) # add a point
            self.sweepD/=(self.period*1000) # correct for sample rate
        else:
            self.sweepD=[0] # derivative is forced to be empty

        # generate the protocol too
        self.generate_protocol()