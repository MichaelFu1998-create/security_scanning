def SetPixelColorsOfRect(self, x: int, y: int, width: int, height: int, colors: Iterable) -> bool:
        """
        x: int.
        y: int.
        width: int.
        height: int.
        colors: Iterable, an iterable list of int values, it's length must equal to width*height.
        Return `ctypes.Array`, an iterable array of int values in argb of the input rect.
        """
        arrayType = ctypes.c_uint32 * (width * height)
        values = arrayType(*colors)
        return bool(_DllClient.instance().dll.BitmapSetPixelsOfRect(ctypes.c_size_t(self._bitmap), x, y, width, height, values))