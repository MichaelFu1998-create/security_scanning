def resolution_str(self):
        '''if set, get the value of resolution as "<n> <period>s", for example: "8 seconds"'''
        if self.resolution is None or isinstance(self.resolution, basestring):
            return self.resolution
        seconds = self.resolution / 1000.
        biggest = self._lookup[0]
        for entry in self._lookup:
            if seconds < entry[1]:
                break
            biggest = entry
        val = seconds / biggest[1]
        if val == int(val):
            val = int(val)
        return '%s %s' % (val, biggest[0])