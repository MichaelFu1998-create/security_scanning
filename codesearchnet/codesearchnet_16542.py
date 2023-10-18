def read(self, filename):
        """Populate the instance from the ccp4 file *filename*."""
        if filename is not None:
            self.filename = filename
        with open(self.filename, 'rb') as ccp4:
            h = self.header = self._read_header(ccp4)
            nentries = h['nc'] * h['nr'] * h['ns']
            # Quick and dirty... slurp it all in one go.
            datafmt = h['bsaflag'] + str(nentries) + self._data_bintype
            a = np.array(struct.unpack(datafmt, ccp4.read(struct.calcsize(datafmt))))
        self.header['filename'] = self.filename
        # TODO: Account for the possibility that y-axis is fastest or
        # slowest index, which unfortunately is possible in CCP4.
        order = 'C' if h['mapc'] == 'z' else 'F'
        self.array = a.reshape(h['nc'], h['nr'], h['ns'], order=order)
        self.delta = self._delta()
        self.origin = np.zeros(3)
        self.rank = 3