def GetSubBitmap(self, x: int, y: int, width: int, height: int) -> 'Bitmap':
        """
        x: int.
        y: int.
        width: int.
        height: int.
        Return `Bitmap`, a sub bitmap of the input rect.
        """
        colors = self.GetPixelColorsOfRect(x, y, width, height)
        bitmap = Bitmap(width, height)
        bitmap.SetPixelColorsOfRect(0, 0, width, height, colors)
        return bitmap