def add_position(self, radial=False, chunksize=2**19, chunkslice='bytes',
                     comp_filter=default_compression, overwrite=False,
                     params=dict()):
        """Add the `position` array in '/trajectories'.
        """
        nparams = self.numeric_params
        num_particles = nparams['np']

        name, ncoords, prefix = 'position', 3, 'X-Y-Z'
        if radial:
            name, ncoords, prefix = 'position_rz', 2, 'R-Z'
        title = '%s position trace of each particle' % prefix
        return self.add_trajectory(name, shape=(num_particles, ncoords, 0),
                                   overwrite=overwrite, chunksize=chunksize,
                                   comp_filter=comp_filter,
                                   atom=tables.Float32Atom(),
                                   title=title,
                                   params=params)