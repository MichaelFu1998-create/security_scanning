def param_particle_pos(self, ind):
        """ Get position of one or more particles """
        ind = self._vps(listify(ind))
        return [self._i2p(i, j) for i in ind for j in ['z', 'y', 'x']]