def figure_protocol(self):
        """plot the current sweep protocol."""
        self.log.debug("creating overlayed protocols plot")
        self.figure()
        plt.plot(self.abf.protoX,self.abf.protoY,color='r')
        self.marginX=0
        self.decorate(protocol=True)