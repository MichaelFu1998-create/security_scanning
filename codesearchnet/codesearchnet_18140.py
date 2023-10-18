def psf_slice(self, zint, size=11, zoffset=0., getextent=False):
        """
        Calculates the 3D psf at a particular z pixel height

        Parameters
        ----------
        zint : float
            z pixel height in image coordinates , converted to 1/k by the
            function using the slab position as well

        size : int, list, tuple
            The size over which to calculate the psf, can be 1 or 3 elements
            for the different axes in image pixel coordinates

        zoffset : float
            Offset in pixel units to use in the calculation of the psf

        cutval : float
            If not None, the psf will be cut along a curve corresponding to
            p(r) == 0 with exponential damping exp(-d^4)

        getextent : boolean
            If True, also return the extent of the psf in pixels for example
            to get the support size. Can only be used with cutval.
        """
        # calculate the current pixel value in 1/k, making sure we are above the slab
        zint = max(self._p2k(self._tz(zint)), 0)
        offset = np.array([zoffset*(zint>0), 0, 0])
        scale = [self.param_dict[self.zscale], 1.0, 1.0]

        # create the coordinate vectors for where to actually calculate the
        tile = util.Tile(left=0, size=size, centered=True)
        vecs = tile.coords(form='flat')
        vecs = [self._p2k(s*i+o) for i,s,o in zip(vecs, scale, offset)]

        psf = self.psffunc(*vecs[::-1], zint=zint, **self.pack_args()).T
        vec = tile.coords(form='meshed')

        # create a smoothly varying point spread function by cutting off the psf
        # at a certain value and smoothly taking it to zero
        if self.cutoffval is not None and not self.cutbyval:
            # find the edges of the PSF
            edge = psf > psf.max() * self.cutoffval
            dd = nd.morphology.distance_transform_edt(~edge)

            # calculate the new PSF and normalize it to the new support
            psf = psf * np.exp(-dd**4)
            psf /= psf.sum()

            if getextent:
                # the size is determined by the edge plus a 2 pad for the
                # exponential damping to zero at the edge
                size = np.array([
                    (vec*edge).min(axis=(1,2,3))-2,
                    (vec*edge).max(axis=(1,2,3))+2,
                ]).T
                return psf, vec, size
            return psf, vec

        # perform a cut by value instead
        if self.cutoffval is not None and self.cutbyval:
            cutval = self.cutoffval * psf.max()

            dd = (psf - cutval) / cutval
            dd[dd > 0] = 0.

            # calculate the new PSF and normalize it to the new support
            psf = psf * np.exp(-(dd / self.cutfallrate)**4)
            psf /= psf.sum()

            # let the small values determine the edges
            edge = psf > cutval * self.cutedgeval
            if getextent:
                # the size is determined by the edge plus a 2 pad for the
                # exponential damping to zero at the edge
                size = np.array([
                    (vec*edge).min(axis=(1,2,3))-2,
                    (vec*edge).max(axis=(1,2,3))+2,
                ]).T
                return psf, vec, size
            return psf, vec

        return psf, vec