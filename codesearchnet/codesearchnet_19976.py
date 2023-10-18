def get_data_around(self,timePoints,thisSweep=False,padding=0.02,msDeriv=0):
        """
        return self.dataY around a time point. All units are seconds.
        if thisSweep==False, the time point is considered to be experiment time
            and an appropriate sweep may be selected. i.e., with 10 second
            sweeps and timePint=35, will select the 5s mark of the third sweep
        """
        if not np.array(timePoints).shape:
            timePoints=[float(timePoints)]
        data=None
        for timePoint in timePoints:
            if thisSweep:
                sweep=self.currentSweep
            else:
                sweep=int(timePoint/self.sweepInterval)
                timePoint=timePoint-sweep*self.sweepInterval
            self.setSweep(sweep)
            if msDeriv:
                dx=int(msDeriv*self.rate/1000) #points per ms
                newData=(self.dataY[dx:]-self.dataY[:-dx])*self.rate/1000/dx
            else:
                newData=self.dataY
            padPoints=int(padding*self.rate)
            pad=np.empty(padPoints)*np.nan
            Ic=timePoint*self.rate #center point (I)
            newData=np.concatenate((pad,pad,newData,pad,pad))
            Ic+=padPoints*2
            newData=newData[Ic-padPoints:Ic+padPoints]
            newData=newData[:int(padPoints*2)] #TODO: omg so much trouble with this!
            if data is None:
                data=[newData]
            else:
                data=np.vstack((data,newData))#TODO: omg so much trouble with this!
        return data