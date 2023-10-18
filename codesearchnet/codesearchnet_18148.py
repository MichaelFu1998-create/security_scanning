def psffunc(self, x, y, z, **kwargs):
        """Calculates a pinhole psf"""
        #do_pinhole?? FIXME
        if self.polychromatic:
            func = psfcalc.calculate_polychrome_pinhole_psf
        else:
            func = psfcalc.calculate_pinhole_psf
        x0, y0 = [psfcalc.vec_to_halfvec(v) for v in [x,y]]
        vls = psfcalc.wrap_and_calc_psf(x0, y0, z, func, **kwargs)
        return vls / vls.sum()