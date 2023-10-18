def add_particle(self, pos, rad):
        """
        Add a particle or list of particles given by a list of positions and
        radii, both need to be array-like.

        Parameters
        ----------
        pos : array-like [N, 3]
            Positions of all new particles

        rad : array-like [N]
            Corresponding radii of new particles

        Returns
        -------
        inds : N-element numpy.ndarray.
            Indices of the added particles.
        """
        rad = listify(rad)
        # add some zero mass particles to the list (same as not having these
        # particles in the image, which is true at this moment)
        inds = np.arange(self.N, self.N+len(rad))
        self.pos = np.vstack([self.pos, pos])
        self.rad = np.hstack([self.rad, np.zeros(len(rad))])

        # update the parameters globally
        self.setup_variables()
        self.trigger_parameter_change()

        # now request a drawing of the particle plz
        params = self.param_particle_rad(inds)
        self.trigger_update(params, rad)
        return inds