def add(self, num_particles, D):
        """Add particles with diffusion coefficient `D` at random positions.
        """
        self._plist += self._generate(num_particles, D, box=self.box,
                                      rs=self.rs)