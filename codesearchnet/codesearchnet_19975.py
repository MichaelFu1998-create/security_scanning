def sweep_decimate(self):
        """
        decimate data using one of the following methods:
            'avg','max','min','fast'
        They're self explainatory. 'fast' just plucks the n'th data point.
        """
        if len(self.dataY)<self.decimateBy:
            return
        if self.decimateMethod:
            points = int(len(self.dataY)/self.decimateBy)
            self.dataY=self.dataY[:points*self.decimateBy]
            self.dataY = np.reshape(self.dataY,(points,self.decimateBy))
            if self.decimateMethod=='avg':
                self.dataY = np.average(self.dataY,1)
            elif self.decimateMethod=='max':
                self.dataY = np.max(self.dataY,1)
            elif self.decimateMethod=='min':
                self.dataY = np.min(self.dataY,1)
            elif self.decimateMethod=='fast':
                self.dataY = self.dataY[:,0]
            else:
                print("!!! METHOD NOT IMPLIMENTED YET!!!",self.decimateMethod)
            self.dataX = np.arange(len(self.dataY))/self.rate*self.decimateBy