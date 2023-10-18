def to_numeric(self, td):
        """
        Convert timedelta to a number corresponding to the
        appropriate units. The appropriate units are those
        determined with the object is initialised.
        """
        if self.package == 'pandas':
            return td.value/NANOSECONDS[self.units]
        else:
            return td.total_seconds()/SECONDS[self.units]