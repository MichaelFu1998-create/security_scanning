def beta(self):
        """
        Courant-Snyder parameter :math:`\\beta`.
        """
        beta = _np.sqrt(self.sx)/self.emit
        return beta