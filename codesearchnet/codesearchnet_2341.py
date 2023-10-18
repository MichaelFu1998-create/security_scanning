def GetPixelColorsOfRow(self, y: int) -> ctypes.Array:
        """
        y: int, row index.
        Return `ctypes.Array`, an iterable array of int values in argb of y row.
        """
        return self.GetPixelColorsOfRect(0, y, self.Width, 1)