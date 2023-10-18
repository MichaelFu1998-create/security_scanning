def _load_dx(self, filename):
        """Initializes Grid from a OpenDX file."""
        dx = OpenDX.field(0)
        dx.read(filename)
        grid, edges = dx.histogramdd()
        self.__init__(grid=grid, edges=edges, metadata=self.metadata)