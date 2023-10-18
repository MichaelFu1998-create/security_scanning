def SetPixelColor(self, x: int, y: int, argb: int) -> bool:
        """
        Set color value of a pixel.
        x: int.
        y: int.
        argb: int, color value.
        Return bool, True if succeed otherwise False.
        """
        return _DllClient.instance().dll.BitmapSetPixel(self._bitmap, x, y, argb)