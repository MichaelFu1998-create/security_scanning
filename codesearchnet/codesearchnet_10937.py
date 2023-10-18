def run(self, rs, overwrite=True, skip_existing=False, path=None,
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
        self.hash_d = hash_(rs.get_state())[:6]   # needed by merge_da()
        print('%s Donor timestamps -    %s' % (header, ctime()), flush=True)
        self.S.simulate_timestamps_mix(
            populations = self.populations,
            max_rates = self.em_rates_d,
            bg_rate = self.bg_rate_d,
            **kwargs)

        # Acceptor timestamps hash is from 'last_random_state' attribute
        # of the donor timestamps. This allows deterministic generation of
        # donor + acceptor timestamps given the input random state.
        ts_d, _ = self.S.get_timestamps_part(self.name_timestamps_d)
        rs.set_state(ts_d.attrs['last_random_state'])
        self.hash_a = hash_(rs.get_state())[:6]   # needed by merge_da()
        print('\n%s Acceptor timestamps - %s' % (header, ctime()), flush=True)
        self.S.simulate_timestamps_mix(
            populations = self.populations,
            max_rates = self.em_rates_a,
            bg_rate = self.bg_rate_a,
            **kwargs)
        print('\n%s Completed. %s' % (header, ctime()), flush=True)