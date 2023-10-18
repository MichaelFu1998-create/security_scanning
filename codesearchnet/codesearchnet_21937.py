def w_p(self):
        """
        Plasma frequency :math:`\\omega_p` for given plasma density
        """
        return _np.sqrt(self.n_p * _np.power(_spc.e, 2) / (_spc.m_e * _spc.epsilon_0))