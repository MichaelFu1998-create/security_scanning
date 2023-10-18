def _sim_trajectories(self, time_size, start_pos, rs,
                          total_emission=False, save_pos=False, radial=False,
                          wrap_func=wrap_periodic):
        """Simulate (in-memory) `time_size` steps of trajectories.

        Simulate Brownian motion diffusion and emission of all the particles.
        Uses the attributes: num_particles, sigma_1d, box, psf.

        Arguments:
            time_size (int): number of time steps to be simulated.
            start_pos (array): shape (num_particles, 3), particles start
                positions. This array is modified to store the end position
                after this method is called.
            rs (RandomState): a `numpy.random.RandomState` object used
                to generate the random numbers.
            total_emission (bool): if True, store only the total emission array
                containing the sum of emission of all the particles.
            save_pos (bool): if True, save the particles 3D trajectories
            wrap_func (function): the function used to apply the boundary
                condition (use :func:`wrap_periodic` or :func:`wrap_mirror`).

        Returns:
            POS (list): list of 3D trajectories arrays (3 x time_size)
            em (array): array of emission (total or per-particle)
        """
        time_size = int(time_size)
        num_particles = self.num_particles
        if total_emission:
            em = np.zeros(time_size, dtype=np.float32)
        else:
            em = np.zeros((num_particles, time_size), dtype=np.float32)

        POS = []
        # pos_w = np.zeros((3, c_size))
        for i, sigma_1d in enumerate(self.sigma_1d):
            delta_pos = rs.normal(loc=0, scale=sigma_1d,
                                  size=3 * time_size)
            delta_pos = delta_pos.reshape(3, time_size)
            pos = np.cumsum(delta_pos, axis=-1, out=delta_pos)
            pos += start_pos[i]

            # Coordinates wrapping using the specified boundary conditions
            for coord in (0, 1, 2):
                pos[coord] = wrap_func(pos[coord], *self.box.b[coord])

            # Sample the PSF along i-th trajectory then square to account
            # for emission and detection PSF.
            Ro = sqrt(pos[0]**2 + pos[1]**2)  # radial pos. on x-y plane
            Z = pos[2]
            current_em = self.psf.eval_xz(Ro, Z)**2
            if total_emission:
                # Add the current particle emission to the total emission
                em += current_em.astype(np.float32)
            else:
                # Store the individual emission of current particle
                em[i] = current_em.astype(np.float32)
            if save_pos:
                pos_save = np.vstack((Ro, Z)) if radial else pos
                POS.append(pos_save[np.newaxis, :, :])
            # Update start_pos in-place for current particle
            start_pos[i] = pos[:, -1:]
        return POS, em