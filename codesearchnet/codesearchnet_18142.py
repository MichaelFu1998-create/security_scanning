def _tz(self, z):
        """ Transform z to real-space coordinates from tile coordinates """
        return (z-self.param_dict['psf-zslab'])*self.param_dict[self.zscale]