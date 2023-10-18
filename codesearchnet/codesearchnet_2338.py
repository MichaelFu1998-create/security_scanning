def GetPixelColorsHorizontally(self, x: int, y: int, count: int) -> ctypes.Array:
        """
        x: int.
        y: int.
        count: int.
        Return `ctypes.Array`, an iterable array of int values in argb form point x,y horizontally.
        """
        arrayType = ctypes.c_uint32 * count
        values = arrayType()
        _DllClient.instance().dll.BitmapGetPixelsHorizontally(ctypes.c_size_t(self._bitmap), x, y, values, count)
        return values