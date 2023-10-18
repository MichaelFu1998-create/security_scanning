def GetPixelColorsOfRect(self, x: int, y: int, width: int, height: int) -> ctypes.Array:
        """
        x: int.
        y: int.
        width: int.
        height: int.
        Return `ctypes.Array`, an iterable array of int values in argb of the input rect.
        """
        arrayType = ctypes.c_uint32 * (width * height)
        values = arrayType()
        _DllClient.instance().dll.BitmapGetPixelsOfRect(ctypes.c_size_t(self._bitmap), x, y, width, height, values)
        return values