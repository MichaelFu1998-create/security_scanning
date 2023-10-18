def set_moments(self, sx, sxp, sxxp):
        """
        Sets the beam moments directly.

        Parameters
        ----------
        sx : float
            Beam moment where :math:`\\text{sx}^2 = \\langle x^2 \\rangle`.
        sxp : float
            Beam moment where :math:`\\text{sxp}^2 = \\langle x'^2 \\rangle`.
        sxxp : float
            Beam moment where :math:`\\text{sxxp} = \\langle x x' \\rangle`.
        """
        self._sx   = sx
        self._sxp  = sxp
        self._sxxp = sxxp
        emit = _np.sqrt(sx**2 * sxp**2 - sxxp**2)
        self._store_emit(emit=emit)