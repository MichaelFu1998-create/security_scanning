def k_ion(self, E):
        """
        Geometric focusing force due to ion column for given plasma density as a function of *E*
        """
        return self.n_p * _np.power(_spc.e, 2) / (2*_sltr.GeV2joule(E) * _spc.epsilon_0)