def figure_protocols(self):
        """plot the protocol of all sweeps."""
        self.log.debug("creating overlayed protocols plot")
        self.figure()
        for sweep in range(self.abf.sweeps):
            self.abf.setsweep(sweep)
            plt.plot(self.abf.protoX,self.abf.protoY,color='r')
        self.marginX=0
        self.decorate(protocol=True)