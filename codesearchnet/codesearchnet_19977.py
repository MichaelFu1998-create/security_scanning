def generate_protocol(self,sweep=None):
        """
        Create (x,y) points necessary to graph protocol for the current sweep.
        """
        #TODO: make a line protocol that's plottable
        if sweep is None:
            sweep = self.currentSweep
        if sweep is None:
            sweep = 0
        if not self.channel in self.header['dictEpochInfoPerDAC'].keys():
            self.protoX=[0,self.sweepSize]
            self.protoY=[self.holding,self.holding]
            self.protoSeqX=self.protoX
            self.protoSeqY=self.protoY
            return
        proto=self.header['dictEpochInfoPerDAC'][self.channel]
        self.protoX=[] #plottable Xs
        self.protoY=[] #plottable Ys
        self.protoX.append(0)
        self.protoY.append(self.holding)
        for step in proto:
            dX = proto[step]['lEpochInitDuration']
            Y = proto[step]['fEpochInitLevel']+proto[step]['fEpochLevelInc']*sweep
            self.protoX.append(self.protoX[-1])
            self.protoY.append(Y) #go to new Y
            self.protoX.append(self.protoX[-1]+dX) #take it to the new X
            self.protoY.append(Y) #update the new Y #TODO: fix for ramps

        if self.header['listDACInfo'][0]['nInterEpisodeLevel']: #nInterEpisodeLevel
            finalVal=self.protoY[-1] #last holding
        else:
            finalVal=self.holding #regular holding
        self.protoX.append(self.protoX[-1])
        self.protoY.append(finalVal)
        self.protoX.append(self.sweepSize)
        self.protoY.append(finalVal)

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

        self.protoX=np.array(self.protoX)
        self.protoY=np.array(self.protoY)