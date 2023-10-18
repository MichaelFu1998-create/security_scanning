def setSweep(self,sweep=0,force=False):
        """Load X/Y data for a particular sweep.
        determines if forced reload is needed, updates currentSweep,
        regenerates dataX (if not None),decimates,returns X/Y.
        Note that setSweep() takes 0.17ms to complete, so go for it!
        """
        if sweep is None or sweep is False:
            sweep=0
        if sweep<0:
            sweep=self.sweeps-sweep #-1 means last sweep
            if sweep<0: #still!
                sweep=0 #first sweep
        if sweep>(self.sweeps-1):
            print(" !! there aren't %d sweeps. Reverting to last (%d) sweep."%(sweep,self.sweeps-1))
            sweep=self.sweeps-1
        sweep=int(sweep)
        try:
            if self.currentSweep==sweep and force==False:
                return
            self.currentSweep=sweep
            self.dataY = self.block.segments[sweep].analogsignals[self.channel]
            self.dataY = np.array(self.dataY)

            B1,B2=self.baseline
            if B1==None:
                B1=0
            else:
                B1=B1*self.rate
            if B2==None:
                B2==self.sweepSize
            else:
                B2=B2*self.rate

                self.dataY-=np.average(self.dataY[self.baseline[0]*self.rate:self.baseline[1]*self.rate])
            self.sweep_genXs()
            self.sweep_decimate()
            self.generate_protocol(sweep=sweep)
            self.dataStart = self.sweepInterval*self.currentSweep
        except Exception:
            print("#"*400,"\n",traceback.format_exc(),'\n',"#"*400)
        return self.dataX,self.dataY