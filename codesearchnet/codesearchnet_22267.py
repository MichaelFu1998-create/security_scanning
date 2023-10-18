def plasma(self, species=_pt.hydrogen):
        """
        The matched :class:`Plasma`.
        """
        return _Plasma(self.n_p, species=species)