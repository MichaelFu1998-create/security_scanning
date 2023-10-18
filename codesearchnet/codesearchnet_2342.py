def GetPixelColorsOfColumn(self, x: int) -> ctypes.Array:
        """
        x: int, column index.
        Return `ctypes.Array`, an iterable array of int values in argb of x column.
        """
        return self.GetPixelColorsOfRect(x, 0, 1, self.Height)