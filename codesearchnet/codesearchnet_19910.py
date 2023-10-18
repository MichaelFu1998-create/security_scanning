def figure_sweeps(self, offsetX=0, offsetY=0):
        """plot every sweep of an ABF file."""
        self.log.debug("creating overlayed sweeps plot")
        self.figure()
        for sweep in range(self.abf.sweeps):
            self.abf.setsweep(sweep)
            self.setColorBySweep()
            plt.plot(self.abf.sweepX2+sweep*offsetX,
                     self.abf.sweepY+sweep*offsetY,
                     **self.kwargs)
        if offsetX:
            self.marginX=.05
        self.decorate()