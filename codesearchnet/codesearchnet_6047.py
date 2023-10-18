def resolution_millis(self):
        '''if set, get the value of resolution in milliseconds'''
        if self.resolution is None or not isinstance(self.resolution, basestring):
                return self.resolution
        val, mult = self.resolution.split(' ')
        return int(float(val) * self._multipier(mult) * 1000)