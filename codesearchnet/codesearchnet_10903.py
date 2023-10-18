def add_emission(self, chunksize=2**19, comp_filter=default_compression,
                     overwrite=False, params=dict(), chunkslice='bytes'):
        """Add the `emission` array in '/trajectories'.
        """
        nparams = self.numeric_params
        num_particles = nparams['np']

        return self.add_trajectory('emission', shape=(num_particles, 0),
                                   overwrite=overwrite, chunksize=chunksize,
                                   comp_filter=comp_filter,
                                   atom=tables.Float32Atom(),
                                   title='Emission trace of each particle',
                                   params=params)