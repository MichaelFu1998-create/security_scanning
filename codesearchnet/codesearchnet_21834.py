def expand_dims(self, axis):
        """Insert a new axis, at a given position in the array shape
        Args:
          axis (int): Position (amongst axes) where new axis is to be inserted.
        """
        if axis == -1:
            axis = self.ndim
        if axis <= self._distaxis:
            subaxis = axis
            new_distaxis = self._distaxis + 1
        else:
            subaxis = axis - 1
            new_distaxis = self._distaxis
        new_subarrays = [expand_dims(ra, subaxis) for ra in self._subarrays]
        return DistArray(new_subarrays, new_distaxis)