def scaled_limits(self):
        """
        Minimum and Maximum to use for computing breaks
        """
        _min = self.limits[0]/self.factor
        _max = self.limits[1]/self.factor
        return _min, _max