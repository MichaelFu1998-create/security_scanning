def _kpad(self, field, finalshape, zpad=False, norm=True):
        """
        fftshift and pad the field with zeros until it has size finalshape.
        if zpad is off, then no padding is put on the z direction. returns
        the fourier transform of the field
        """
        currshape = np.array(field.shape)

        if any(finalshape < currshape):
            raise IndexError("PSF tile size is less than minimum support size")

        d = finalshape - currshape

        # fix off-by-one issues when going odd to even tile sizes
        o = d % 2
        d = np.floor_divide(d, 2)

        if not zpad:
            o[0] = 0

        axes = None
        pad = tuple((d[i]+o[i],d[i]) for i in [0,1,2])
        rpsf = np.pad(field, pad, mode='constant', constant_values=0)
        rpsf = np.fft.ifftshift(rpsf, axes=axes)
        kpsf = fft.rfftn(rpsf, **fftkwargs)

        if norm:
            kpsf /= kpsf[0,0,0]
        return kpsf