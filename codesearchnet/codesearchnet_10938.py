def run_da(self, rs, overwrite=True, skip_existing=False, path=None,
               chunksize=None):
        """Compute timestamps for current populations."""
        if path is None:
            path = str(self.S.store.filepath.parent)
        kwargs = dict(rs=rs, overwrite=overwrite, path=path,
                      timeslice=self.timeslice, skip_existing=skip_existing)
        if chunksize is not None:
            kwargs['chunksize'] = chunksize
        header = ' - Mixture Simulation:'

        # Donor timestamps hash is from the input RandomState
        self._calc_hash_da(rs)
        print('%s Donor + Acceptor timestamps - %s' %
              (header, ctime()), flush=True)
        self.S.simulate_timestamps_mix_da(
            max_rates_d = self.em_rates_d,
            max_rates_a = self.em_rates_a,
            populations = self.populations,
            bg_rate_d = self.bg_rate_d,
            bg_rate_a = self.bg_rate_a,
            **kwargs)
        print('\n%s Completed. %s' % (header, ctime()), flush=True)