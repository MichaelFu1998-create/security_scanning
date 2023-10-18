def kvectors(self, norm=False, form='broadcast', real=False, shift=False):
        """
        Return the kvectors associated with this tile, given the standard form
        of -0.5 to 0.5. `norm` and `form` arguments arethe same as that passed to
        `Tile.coords`.

        Parameters
        -----------
        real : boolean
            whether to return kvectors associated with the real fft instead
        """
        if norm is False:
            norm = 1
        if norm is True:
            norm = np.array(self.shape)
        norm = aN(norm, self.dim, dtype='float')

        v = list(np.fft.fftfreq(self.shape[i])/norm[i] for i in range(self.dim))

        if shift:
            v = list(np.fft.fftshift(t) for t in v)

        if real:
            v[-1] = v[-1][:(self.shape[-1]+1)//2]

        return self._format_vector(v, form=form)