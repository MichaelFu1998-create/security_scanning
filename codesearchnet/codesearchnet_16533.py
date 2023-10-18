def _load_cpp4(self, filename):
        """Initializes Grid from a CCP4 file."""
        ccp4 = CCP4.CCP4()
        ccp4.read(filename)
        grid, edges = ccp4.histogramdd()
        self.__init__(grid=grid, edges=edges, metadata=self.metadata)