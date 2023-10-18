def sweep_genXs(self):
        """generate sweepX (in seconds) to match sweepY"""
        if self.decimateMethod:
            self.dataX=np.arange(len(self.dataY))/self.rate
            self.dataX*=self.decimateBy
            return
        if self.dataX is None or len(self.dataX)!=len(self.dataY):
            self.dataX=np.arange(len(self.dataY))/self.rate