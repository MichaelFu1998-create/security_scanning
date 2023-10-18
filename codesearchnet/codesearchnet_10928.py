def simulate_timestamps_mix(self, max_rates, populations, bg_rate,
                                rs=None, seed=1, chunksize=2**16,
                                comp_filter=None, overwrite=False,
                                skip_existing=False, scale=10,
                                path=None, t_chunksize=None, timeslice=None):
        """Compute one timestamps array for a mixture of N populations.

        Timestamp data are saved to disk and accessible as pytables arrays in
        `._timestamps` and `._tparticles`.
        The background generated timestamps are assigned a
        conventional particle number (last particle index + 1).

        Arguments:
            max_rates (list): list of the peak max emission rate for each
                population.
            populations (list of slices): slices to `self.particles`
                defining each population.
            bg_rate (float, cps): rate for a Poisson background process
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

        name = self._get_ts_name_mix(max_rates, populations, bg_rate, rs=rs)
        kw = dict(name=name, clk_p=self.t_step / scale,
                  max_rates=max_rates, bg_rate=bg_rate, populations=populations,
                  num_particles=self.num_particles,
                  bg_particle=self.num_particles,
                  overwrite=overwrite, chunksize=chunksize)
        if comp_filter is not None:
            kw.update(comp_filter=comp_filter)
        try:
            self._timestamps, self._tparticles = (self.ts_store
                                                  .add_timestamps(**kw))
        except ExistingArrayError as e:
            if skip_existing:
                print(' - Skipping already present timestamps array.')
                return
            else:
                raise e

        self.ts_group._v_attrs['init_random_state'] = rs.get_state()
        self._timestamps.attrs['init_random_state'] = rs.get_state()
        self._timestamps.attrs['PyBroMo'] = __version__

        ts_list, part_list = [], []
        # Load emission in chunks, and save only the final timestamps
        bg_rates = [None] * (len(max_rates) - 1) + [bg_rate]
        prev_time = 0
        for i_start, i_end in iter_chunk_index(timeslice_size, t_chunksize):

            curr_time = np.around(i_start * self.t_step, decimals=0)
            if curr_time > prev_time:
                print(' %.1fs' % curr_time, end='', flush=True)
                prev_time = curr_time

            em_chunk = self.emission[:, i_start:i_end]

            times_chunk_s, par_index_chunk_s = \
                self._sim_timestamps_populations(
                    em_chunk, max_rates, populations, bg_rates, i_start,
                    rs, scale)

            # Save sorted timestamps (suffix '_s') and corresponding particles
            ts_list.append(times_chunk_s)
            part_list.append(par_index_chunk_s)

        for ts, part in zip(ts_list, part_list):
            self._timestamps.append(ts)
            self._tparticles.append(part)

        # Save current random state so it can be resumed in the next session
        self.ts_group._v_attrs['last_random_state'] = rs.get_state()
        self._timestamps.attrs['last_random_state'] = rs.get_state()
        self.ts_store.h5file.flush()