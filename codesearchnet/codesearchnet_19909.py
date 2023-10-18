def figure_chronological(self):
        """plot every sweep of an ABF file (with comments)."""
        self.log.debug("creating chronological plot")
        self.figure()
        for sweep in range(self.abf.sweeps):
            self.abf.setsweep(sweep)
            self.setColorBySweep()
            if self.abf.derivative:
                plt.plot(self.abf.sweepX,self.abf.sweepD,**self.kwargs)
            else:
                plt.plot(self.abf.sweepX,self.abf.sweepY,**self.kwargs)
        self.comments()
        self.decorate()