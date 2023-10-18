def numeric_to_timedelta(self, numerics):
        """
        Convert sequence of numerics to timedelta
        """
        if self.package == 'pandas':
            return [self.type(int(x*self.factor), units='ns')
                    for x in numerics]
        else:
            return [self.type(seconds=x*self.factor)
                    for x in numerics]