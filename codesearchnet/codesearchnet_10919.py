def compact_name_core(self, hashsize=6, t_max=False):
        """Compact representation of simulation params (no ID, EID and t_max)
        """
        Moles = self.concentration()
        name = "%s_%dpM_step%.1fus" % (
            self.particles.short_repr(), Moles * 1e12, self.t_step * 1e6)
        if hashsize > 0:
            name = self.hash()[:hashsize] + '_' + name
        if t_max:
            name += "_t_max%.1fs" % self.t_max
        return name