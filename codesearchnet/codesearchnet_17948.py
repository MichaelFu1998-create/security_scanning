def _update_type(self, params):
        """ Returns dozscale and particle list of update """
        dozscale = False
        particles = []
        for p in listify(params):
            typ, ind = self._p2i(p)
            particles.append(ind)
            dozscale = dozscale or typ == 'zscale'
        particles = set(particles)
        return dozscale, particles