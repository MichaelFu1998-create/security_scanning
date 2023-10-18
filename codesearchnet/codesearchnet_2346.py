def GetAllPixelColors(self) -> ctypes.Array:
        """
        Return `ctypes.Array`, an iterable array of int values in argb.
        """
        return self.GetPixelColorsOfRect(0, 0, self.Width, self.Height)