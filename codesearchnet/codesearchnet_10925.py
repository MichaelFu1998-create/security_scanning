def simulate_diffusion(self, save_pos=False, total_emission=True,
                           radial=False, rs=None, seed=1, path='./',
                           wrap_func=wrap_periodic,
                           chunksize=2**19, chunkslice='times', verbose=True):
        """Simulate Brownian motion trajectories and emission rates.

        This method performs the Brownian motion simulation using the current
        set of parameters. Before running this method you can check the
        disk-space requirements using :method:`print_sizes`.

        Results are stored to disk in HDF5 format and are accessible in
        in `self.emission`, `self.emission_tot` and `self.position` as
        pytables arrays.

        Arguments:
            save_pos (bool): if True, save the particles 3D trajectories
            total_emission (bool): if True, store only the total emission array
                containing the sum of emission of all the particles.
            rs (RandomState object): random state object used as random number
                generator. If None, use a random state initialized from seed.
            seed (uint): when `rs` is None, `seed` is used to initialize the
                random state, otherwise is ignored.
            wrap_func (function): the function used to apply the boundary
                condition (use :func:`wrap_periodic` or :func:`wrap_mirror`).
            path (string): a folder where simulation data is saved.
            verbose (bool): if False, prints no output.
        """
        if rs is None:
            rs = np.random.RandomState(seed=seed)
        self.open_store_traj(chunksize=chunksize, chunkslice=chunkslice,
                             radial=radial, path=path)
        # Save current random state for reproducibility
        self.traj_group._v_attrs['init_random_state'] = rs.get_state()

        em_store = self.emission_tot if total_emission else self.emission

        print('- Start trajectories simulation - %s' % ctime(), flush=True)
        if verbose:
            print('[PID %d] Diffusion time:' % os.getpid(), end='')
        i_chunk = 0
        t_chunk_size = self.emission.chunkshape[1]
        chunk_duration = t_chunk_size * self.t_step

        par_start_pos = self.particles.positions
        prev_time = 0
        for time_size in iter_chunksize(self.n_samples, t_chunk_size):
            if verbose:
                curr_time = int(chunk_duration * (i_chunk + 1))
                if curr_time > prev_time:
                    print(' %ds' % curr_time, end='', flush=True)
                    prev_time = curr_time

            POS, em = self._sim_trajectories(time_size, par_start_pos, rs,
                                             total_emission=total_emission,
                                             save_pos=save_pos, radial=radial,
                                             wrap_func=wrap_func)

            ## Append em to the permanent storage
            # if total_emission, data is just a linear array
            # otherwise is a 2-D array (self.num_particles, c_size)
            em_store.append(em)
            if save_pos:
                self.position.append(np.vstack(POS).astype('float32'))
            i_chunk += 1
            self.store.h5file.flush()

        # Save current random state
        self.traj_group._v_attrs['last_random_state'] = rs.get_state()
        self.store.h5file.flush()
        print('\n- End trajectories simulation - %s' % ctime(), flush=True)