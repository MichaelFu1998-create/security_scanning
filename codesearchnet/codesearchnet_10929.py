def simulate_timestamps_mix_da(self, max_rates_d, max_rates_a,
                                   populations, bg_rate_d, bg_rate_a,
                                   rs=None, seed=1, chunksize=2**16,
                                   comp_filter=None, overwrite=False,
                                   skip_existing=False, scale=10,
                                   path=None, t_chunksize=2**19,
                                   timeslice=None):

        """Compute D and A timestamps arrays for a mixture of N populations.

        This method reads the emission from disk once, and generates a pair
        of timestamps arrays (e.g. donor and acceptor) from each chunk.

        Timestamp data are saved to disk and accessible as pytables arrays in
        `._timestamps_d/a` and `._tparticles_d/a`.
        The background generated timestamps are assigned a
        conventional particle number (last particle index + 1).

        Arguments:
            max_rates_d (list): list of the peak max emission rate in the
                donor channel for each population.
            max_rates_a (list): list of the peak max emission rate in the
                acceptor channel for each population.
            populations (list of slices): slices to `self.particles`
                defining each population.
            bg_rate_d (float, cps): rate for a Poisson background process
                in the donor channel.
            bg_rate_a (float, cps): rate for a Poisson background process
                in the acceptor channel.
            rs (RandomState object): random state object used as random number
                generator. If None, use a random state initialized from seed.
            seed (uint): when `rs` is None, `seed` is used to initialize the
                random state, otherwise is ignored.
            chunksize (int): chunk size used for the on-disk timestamp array
            comp_filter (tables.Filter or None): compression filter to use
                for the on-disk `timestamps` and `tparticles` arrays.
                If None use default compression.
            overwrite (bool): if True, overwrite any pre-existing timestamps
                array. If False, never overwrite. The outcome of simulating an
                existing array is controlled by `skip_existing` flag.
            skip_existing (bool): if True, skip simulation if the same
                timestamps array is already present.
            scale (int): `self.t_step` is multiplied by `scale` to obtain the
                timestamps units in seconds.
            path (string): folder where to save the data.
            timeslice (float or None): timestamps are simulated until
                `timeslice` seconds. If None, simulate until `self.t_max`.
        """
        self.open_store_timestamp(chunksize=chunksize, path=path)
        rs = self._get_group_randomstate(rs, seed, self.ts_group)
        if t_chunksize is None:
            t_chunksize = self.emission.chunkshape[1]
        timeslice_size = self.n_samples
        if timeslice is not None:
            timeslice_size = timeslice // self.t_step

        name_d = self._get_ts_name_mix(max_rates_d, populations, bg_rate_d, rs)
        name_a = self._get_ts_name_mix(max_rates_a, populations, bg_rate_a, rs)

        kw = dict(clk_p=self.t_step / scale,
                  populations=populations,
                  num_particles=self.num_particles,
                  bg_particle=self.num_particles,
                  overwrite=overwrite, chunksize=chunksize)
        if comp_filter is not None:
            kw.update(comp_filter=comp_filter)

        kw.update(name=name_d, max_rates=max_rates_d, bg_rate=bg_rate_d)
        try:
            self._timestamps_d, self._tparticles_d = (self.ts_store
                                                      .add_timestamps(**kw))
        except ExistingArrayError as e:
            if skip_existing:
                print(' - Skipping already present timestamps array.')
                return
            else:
                raise e

        kw.update(name=name_a, max_rates=max_rates_a, bg_rate=bg_rate_a)
        try:
            self._timestamps_a, self._tparticles_a = (self.ts_store
                                                      .add_timestamps(**kw))
        except ExistingArrayError as e:
            if skip_existing:
                print(' - Skipping already present timestamps array.')
                return
            else:
                raise e

        self.ts_group._v_attrs['init_random_state'] = rs.get_state()
        self._timestamps_d.attrs['init_random_state'] = rs.get_state()
        self._timestamps_d.attrs['PyBroMo'] = __version__
        self._timestamps_a.attrs['init_random_state'] = rs.get_state()
        self._timestamps_a.attrs['PyBroMo'] = __version__

        # Load emission in chunks, and save only the final timestamps
        bg_rates_d = [None] * (len(max_rates_d) - 1) + [bg_rate_d]
        bg_rates_a = [None] * (len(max_rates_a) - 1) + [bg_rate_a]
        prev_time = 0
        for i_start, i_end in iter_chunk_index(timeslice_size, t_chunksize):

            curr_time = np.around(i_start * self.t_step, decimals=1)
            if curr_time > prev_time:
                print(' %.1fs' % curr_time, end='', flush=True)
                prev_time = curr_time

            em_chunk = self.emission[:, i_start:i_end]

            times_chunk_s_d, par_index_chunk_s_d = \
                self._sim_timestamps_populations(
                    em_chunk, max_rates_d, populations, bg_rates_d, i_start,
                    rs, scale)

            times_chunk_s_a, par_index_chunk_s_a = \
                self._sim_timestamps_populations(
                    em_chunk, max_rates_a, populations, bg_rates_a, i_start,
                    rs, scale)

            # Save sorted timestamps (suffix '_s') and corresponding particles
            self._timestamps_d.append(times_chunk_s_d)
            self._tparticles_d.append(par_index_chunk_s_d)
            self._timestamps_a.append(times_chunk_s_a)
            self._tparticles_a.append(par_index_chunk_s_a)

        # Save current random state so it can be resumed in the next session
        self.ts_group._v_attrs['last_random_state'] = rs.get_state()
        self._timestamps_d._v_attrs['last_random_state'] = rs.get_state()
        self.ts_store.h5file.flush()