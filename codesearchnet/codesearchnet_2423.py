def ToBitmap(self, x: int = 0, y: int = 0, width: int = 0, height: int = 0) -> Bitmap:
        """
        Capture control to a Bitmap object.
        x, y: int, the point in control's internal position(from 0,0).
        width, height: int, image's width and height from x, y, use 0 for entire area.
                       If width(or height) < 0, image size will be control's width(or height) - width(or height).
        """
        bitmap = Bitmap()
        bitmap.FromControl(self, x, y, width, height)
        return bitmap