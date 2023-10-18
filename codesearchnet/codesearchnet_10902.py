def add_emission_tot(self, chunksize=2**19, comp_filter=default_compression,
                         overwrite=False, params=dict(),
                         chunkslice='bytes'):
        """Add the `emission_tot` array in '/trajectories'.
        """
        kwargs = dict(overwrite=overwrite, chunksize=chunksize, params=params,
                      comp_filter=comp_filter, atom=tables.Float32Atom(),
                      title='Summed emission trace of all the particles')
        return self.add_trajectory('emission_tot', **kwargs)