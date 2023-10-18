def reset(self, new_region_size=None, do_calc_size=True, new_damping=None,
            new_max_mem=None):
        """
        Resets the particle groups and optionally the region size and damping.

        Parameters
        ----------
            new_region_size : : Int or 3-element list-like of ints, optional
                The region size for sub-blocking particles. Default is 40
            do_calc_size : Bool, optional
                If True, calculates the region size internally based on
                the maximum allowed memory. Default is True
            new_damping : Float or None, optional
                The new damping of the optimizer. Set to None to leave
                as the default for LMParticles. Default is None.
            new_max_mem : Numeric, optional
                The maximum allowed memory for J to occupy. Default is 1e9
        """
        if new_region_size is not None:
            self.region_size = new_region_size
        if new_max_mem != None:
            self.max_mem = new_max_mem
        if do_calc_size:
            self.region_size = calc_particle_group_region_size(self.state,
                    region_size=self.region_size, max_mem=self.max_mem)
        self.stats = []
        self.particle_groups = separate_particles_into_groups(self.state,
                self.region_size, doshift='rand')
        if new_damping is not None:
            self._kwargs.update({'damping':new_damping})
        if self.save_J:
            if len(self.particle_groups) > 90:
                CLOG.warn('Attempting to create many open files. Consider increasing max_mem and/or region_size to avoid crashes.')
            self._tempfiles = []
            self._has_saved_J = []
            for a in range(len(self.particle_groups)):
                #TemporaryFile is automatically deleted
                for _ in ['j','tile']:
                    self._tempfiles.append(tempfile.TemporaryFile(dir=os.getcwd()))
                self._has_saved_J.append(False)