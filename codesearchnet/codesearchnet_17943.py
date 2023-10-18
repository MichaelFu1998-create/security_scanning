def param_particle(self, ind):
        """ Get position and radius of one or more particles """
        ind = self._vps(listify(ind))
        return [self._i2p(i, j) for i in ind for j in ['z', 'y', 'x', 'a']]