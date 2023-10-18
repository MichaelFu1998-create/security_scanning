def read(self, filename):
        """Populate the instance from the plt file *filename*."""
        from struct import calcsize, unpack
        if not filename is None:
            self.filename = filename
        with open(self.filename, 'rb') as plt:
            h = self.header = self._read_header(plt)
            nentries = h['nx'] * h['ny'] * h['nz']
            # quick and dirty... slurp it all in one go
            datafmt = h['bsaflag']+str(nentries)+self._data_bintype
            a = numpy.array(unpack(datafmt, plt.read(calcsize(datafmt))))
        self.header['filename'] = self.filename
        self.array = a.reshape(h['nz'], h['ny'], h['nx']).transpose()  # unpack plt in reverse!!
        self.delta = self._delta()
        self.origin = numpy.array([h['xmin'], h['ymin'], h['zmin']]) + 0.5*numpy.diagonal(self.delta)
        self.rank = h['rank']