def initialize(self):
        """Start from scratch and initialize all objects / draw self.particles"""
        self.particles = np.zeros(self.shape.shape, dtype=self.float_precision)

        for p0, arg0 in zip(self.pos, self._drawargs()):
            self._draw_particle(p0, *listify(arg0))