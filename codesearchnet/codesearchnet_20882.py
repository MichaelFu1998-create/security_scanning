def load_markers(self, filename, attachments, max_frames=1e100):
        '''Load marker data and attachment preferences into the model.

        Parameters
        ----------
        filename : str
            The name of a file containing marker data. This currently needs to
            be either a .C3D or a .CSV file. CSV files must adhere to a fairly
            strict column naming convention; see :func:`Markers.load_csv` for
            more information.
        attachments : str
            The name of a text file specifying how markers are attached to
            skeleton bodies.
        max_frames : number, optional
            Only read in this many frames of marker data. By default, the entire
            data file is read into memory.

        Returns
        -------
        markers : :class:`Markers`
            Returns a markers object containing loaded marker data as well as
            skeleton attachment configuration.
        '''
        self.markers = Markers(self)
        fn = filename.lower()
        if fn.endswith('.c3d'):
            self.markers.load_c3d(filename, max_frames=max_frames)
        elif fn.endswith('.csv') or fn.endswith('.csv.gz'):
            self.markers.load_csv(filename, max_frames=max_frames)
        else:
            logging.fatal('%s: not sure how to load markers!', filename)
        self.markers.load_attachments(attachments, self.skeleton)