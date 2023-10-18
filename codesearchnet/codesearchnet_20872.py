def load_csv(self, filename, start_frame=10, max_frames=int(1e300)):
        '''Load marker data from a CSV file.

        The file will be imported using Pandas, which must be installed to use
        this method. (``pip install pandas``)

        The first line of the CSV file will be used for header information. The
        "time" column will be used as the index for the data frame. There must
        be columns named 'markerAB-foo-x','markerAB-foo-y','markerAB-foo-z', and
        'markerAB-foo-c' for marker 'foo' to be included in the model.

        Parameters
        ----------
        filename : str
            Name of the CSV file to load.
        '''
        import pandas as pd

        compression = None
        if filename.endswith('.gz'):
            compression = 'gzip'
        df = pd.read_csv(filename, compression=compression).set_index('time').fillna(-1)

        # make sure the data frame's time index matches our world.
        assert self.world.dt == pd.Series(df.index).diff().mean()

        markers = []
        for c in df.columns:
            m = re.match(r'^marker\d\d-(.*)-c$', c)
            if m:
                markers.append(m.group(1))
        self.channels = self._map_labels_to_channels(markers)

        cols = [c for c in df.columns if re.match(r'^marker\d\d-.*-[xyzc]$', c)]
        self.data = df[cols].values.reshape((len(df), len(markers), 4))[start_frame:]
        self.data[:, :, [1, 2]] = self.data[:, :, [2, 1]]

        logging.info('%s: loaded marker data %s', filename, self.data.shape)
        self.process_data()
        self.create_bodies()