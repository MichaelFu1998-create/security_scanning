def set_Courant_Snyder(self, beta, alpha, emit=None, emit_n=None):
        """
        Sets the beam moments indirectly using Courant-Snyder parameters.

        Parameters
        ----------
        beta : float
            Courant-Snyder parameter :math:`\\beta`.
        alpha : float
            Courant-Snyder parameter :math:`\\alpha`.
        emit : float
            Beam emittance :math:`\\epsilon`.
        emit_n : float
            Normalized beam emittance :math:`\\gamma \\epsilon`.
        """

        self._store_emit(emit=emit, emit_n=emit_n)
        
        self._sx   = _np.sqrt(beta*self.emit)
        self._sxp  = _np.sqrt((1+alpha**2)/beta*self.emit)
        self._sxxp = -alpha*self.emit