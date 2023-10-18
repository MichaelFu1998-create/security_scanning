def _sim_timestamps(self, max_rate, bg_rate, emission, i_start, rs,
                        ip_start=0, scale=10, sort=True):
        """Simulate timestamps from emission trajectories.

        Uses attributes: `.t_step`.

        Returns:
            A tuple of two arrays: timestamps and particles.
        """
        counts_chunk = sim_timetrace_bg(emission, max_rate, bg_rate,
                                        self.t_step, rs=rs)
        nrows = emission.shape[0]
        if bg_rate is not None:
            nrows += 1
        assert counts_chunk.shape == (nrows, emission.shape[1])
        max_counts = counts_chunk.max()
        if max_counts == 0:
            return np.array([], dtype=np.int64), np.array([], dtype=np.int64)

        time_start = i_start * scale
        time_stop = time_start + counts_chunk.shape[1] * scale
        ts_range = np.arange(time_start, time_stop, scale, dtype='int64')

        # Loop for each particle to compute timestamps
        times_chunk_p = []
        par_index_chunk_p = []
        for ip, counts_chunk_ip in enumerate(counts_chunk):
            # Compute timestamps for particle ip for all bins with counts
            times_c_ip = []
            for v in range(1, max_counts + 1):
                times_c_ip.append(ts_range[counts_chunk_ip >= v])

            # Stack the timestamps from different "counts"
            t = np.hstack(times_c_ip)
            # Append current particle
            times_chunk_p.append(t)
            par_index_chunk_p.append(np.full(t.size, ip + ip_start, dtype='u1'))

        # Merge the arrays of different particles
        times_chunk = np.hstack(times_chunk_p)
        par_index_chunk = np.hstack(par_index_chunk_p)

        if sort:
            # Sort timestamps inside the merged chunk
            index_sort = times_chunk.argsort(kind='mergesort')
            times_chunk = times_chunk[index_sort]
            par_index_chunk = par_index_chunk[index_sort]

        return times_chunk, par_index_chunk