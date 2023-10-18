def psffunc(self, *args, **kwargs):
        """Calculates a linescan psf"""
        if self.polychromatic:
            func = psfcalc.calculate_polychrome_linescan_psf
        else:
            func = psfcalc.calculate_linescan_psf
        return func(*args, **kwargs)