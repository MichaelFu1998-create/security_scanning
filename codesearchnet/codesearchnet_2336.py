def GetPixelColor(self, x: int, y: int) -> int:
        """
        Get color value of a pixel.
        x: int.
        y: int.
        Return int, argb color.
        b = argb & 0x0000FF
        g = (argb & 0x00FF00) >> 8
        r = (argb & 0xFF0000) >> 16
        a = (argb & 0xFF0000) >> 24
        """
        return _DllClient.instance().dll.BitmapGetPixel(self._bitmap, x, y)