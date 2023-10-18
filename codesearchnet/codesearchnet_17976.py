def kcenter(self):
        """ Return the frequency center of the tile (says fftshift) """
        return np.array([
            np.abs(np.fft.fftshift(np.fft.fftfreq(q))).argmin()
            for q in self.shape
        ]).astype('float')