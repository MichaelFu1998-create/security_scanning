def load_c3d(self, filename, start_frame=0, max_frames=int(1e300)):
        '''Load marker data from a C3D file.

        The file will be imported using the c3d module, which must be installed
        to use this method. (``pip install c3d``)

        Parameters
        ----------
        filename : str
            Name of the C3D file to load.
        start_frame : int, optional
            Discard the first N frames. Defaults to 0.
        max_frames : int, optional
            Maximum number of frames to load. Defaults to loading all frames.
        '''
        import c3d

        with open(filename, 'rb') as handle:
            reader = c3d.Reader(handle)

            logging.info('world frame rate %s, marker frame rate %s',
                         1 / self.world.dt, reader.point_rate)

            # set up a map from marker label to index in the data stream.
            self.channels = self._map_labels_to_channels([
                s.strip() for s in reader.point_labels])

            # read the actual c3d data into a numpy array.
            data = []
            for i, (_, frame, _) in enumerate(reader.read_frames()):
                if i >= start_frame:
                    data.append(frame[:, [0, 1, 2, 4]])
                if len(data) > max_frames:
                    break
            self.data = np.array(data)

            # scale the data to meters -- mm is a very common C3D unit.
            if reader.get('POINT:UNITS').string_value.strip().lower() == 'mm':
                logging.info('scaling point data from mm to m')
                self.data[:, :, :3] /= 1000.

        logging.info('%s: loaded marker data %s', filename, self.data.shape)
        self.process_data()
        self.create_bodies()