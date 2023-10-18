def measure_size_drift(self, z, size=31, zoffset=0.):
        """ Returns the 'size' of the psf in each direction a particular z (px) """
        drift = 0.0
        for i in range(self.measurement_iterations):
            psf, vec = self.psf_slice(z, size=size, zoffset=zoffset+drift)
            psf = psf / psf.sum()

            drift += moment(psf, vec[0], order=1)
            psize = [moment(psf, j, order=2) for j in vec]
        return np.array(psize), drift