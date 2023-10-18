def _load_plt(self, filename):
        """Initialize Grid from gOpenMol plt file."""
        g = gOpenMol.Plt()
        g.read(filename)
        grid, edges = g.histogramdd()
        self.__init__(grid=grid, edges=edges, metadata=self.metadata)