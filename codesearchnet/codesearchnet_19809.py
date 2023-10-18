def generate_protocol(self):
        """
        Recreate the command stimulus (protocol) for the current sweep.
        It's not stored point by point (that's a waste of time and memory!)
        Instead it's stored as a few (x,y) points which can be easily graphed.

        TODO: THIS
        for segment in abf.ABFreader.read_protocol():
            for analogsignal in segment.analogsignals:
                print(analogsignal)
                plt.plot(analogsignal)
                plt.show()
                plt.close('all')

        """
        # TODO: elegantly read the protocol like this:
            #abf.ABFreader.read_protocol()[0].analogsignals()[sigNum]



        # TODO: right now this works only for the first channel

        # correct for weird recording/protocol misalignment
        #what is magic here? 64-bit data points? #1,000,000/64 = 15625 btw
        self.offsetX = int(self.sweepSize/64)

        # if there's not a header, get out of here!
        if not len(self.header['dictEpochInfoPerDAC']):
            self.log.debug("no protocol defined, so I'll make one")
            self.protoX,self.protoY=[0,self.sweepX[-1]],[self.holding,self.holding]
            self.protoSeqX,self.protoSeqY=[0],[self.holding]
            return

        # load our protocol from the header
        proto=self.header['dictEpochInfoPerDAC'][self.channel]

        # prepare our (x,y) pair arrays
        self.protoX,self.protoY=[] ,[]

        # assume our zero time point is the "holding" value
        self.protoX.append(0)
        self.protoY.append(self.holding) #TODO: what is this???

        # now add x,y points for each change in the protocol
        for step in proto:
            dX = proto[step]['lEpochInitDuration']
            Y = proto[step]['fEpochInitLevel']+proto[step]['fEpochLevelInc']*self.sweep
            # we have a new Y value, so add it to the last time point
            self.protoX.append(self.protoX[-1])
            self.protoY.append(Y)
            # now add the same Y point after "dX" amount of time
            self.protoX.append(self.protoX[-1]+dX)
            self.protoY.append(Y)
            # TODO: detect ramps and warn what's up

        # The last point is probably holding current
        finalVal=self.holding #regular holding
        # although if it's set to "use last value", maybe that should be the last one
        if self.header['listDACInfo'][0]['nInterEpisodeLevel']:
            finalVal=self.protoY[-1]

        # add the shift to the final value to the list
        self.protoX.append(self.protoX[-1])
        self.protoY.append(finalVal)
        # and again as the very last time point
        self.protoX.append(self.sweepSize)
        self.protoY.append(finalVal)

        # update the sequence of protocols now (eliminate duplicate entries)
        for i in range(1,len(self.protoX)-1): #correct for weird ABF offset issue.
            self.protoX[i]=self.protoX[i]+self.offsetX
        self.protoSeqY=[self.protoY[0]]
        self.protoSeqX=[self.protoX[0]]
        for i in range(1,len(self.protoY)):
            if not self.protoY[i]==self.protoY[i-1]:
                self.protoSeqY.append(self.protoY[i])
                self.protoSeqX.append(self.protoX[i])
        if self.protoY[0]!=self.protoY[1]:
            self.protoY.insert(1,self.protoY[0])
            self.protoX.insert(1,self.protoX[1])
            self.protoY.insert(1,self.protoY[0])
            self.protoX.insert(1,self.protoX[0]+self.offsetX/2)
        self.protoSeqY.append(finalVal)
        self.protoSeqX.append(self.sweepSize)

        # convert lists to numpy arrays and do any final conversions
        self.protoX=np.array(self.protoX)/self.pointsPerSec
        self.protoY=np.array(self.protoY)