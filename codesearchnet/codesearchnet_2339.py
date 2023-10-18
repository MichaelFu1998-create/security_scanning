def SetPixelColorsHorizontally(self, x: int, y: int, colors: Iterable) -> bool:
        """
        Set pixel colors form x,y horizontally.
        x: int.
        y: int.
        colors: Iterable, an iterable list of int color values in argb.
        Return bool, True if succeed otherwise False.
        """
        count = len(colors)
        arrayType = ctypes.c_uint32 * count
        values = arrayType(*colors)
        return _DllClient.instance().dll.BitmapSetPixelsHorizontally(ctypes.c_size_t(self._bitmap), x, y, values, count)