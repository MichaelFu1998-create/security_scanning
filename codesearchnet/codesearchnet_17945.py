def param_particle_rad(self, ind):
        """ Get radius of one or more particles """
        ind = self._vps(listify(ind))
        return [self._i2p(i, 'a') for i in ind]