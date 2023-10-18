def remove_particle(self, inds):
        """
        Remove the particle at index `inds`, may be a list.
        Returns [3,N], [N] element numpy.ndarray of pos, rad.
        """
        if self.rad.shape[0] == 0:
            return

        inds = listify(inds)

        # Here's the game plan:
        #   1. get all positions and sizes of particles that we will be
        #      removing (to return to user)
        #   2. redraw those particles to 0.0 radius
        #   3. remove the particles and trigger changes
        # However, there is an issue -- if there are two particles at opposite
        # ends of the image, it will be significantly slower than usual
        pos = self.pos[inds].copy()
        rad = self.rad[inds].copy()

        self.trigger_update(self.param_particle_rad(inds), np.zeros(len(inds)))

        self.pos = np.delete(self.pos, inds, axis=0)
        self.rad = np.delete(self.rad, inds, axis=0)

        # update the parameters globally
        self.setup_variables()
        self.trigger_parameter_change()
        return np.array(pos).reshape(-1,3), np.array(rad).reshape(-1)