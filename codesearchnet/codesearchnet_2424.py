def CaptureToImage(self, savePath: str, x: int = 0, y: int = 0, width: int = 0, height: int = 0) -> bool:
        """
        Capture control to a image file.
        savePath: str, should end with .bmp, .jpg, .jpeg, .png, .gif, .tif, .tiff.
        x, y: int, the point in control's internal position(from 0,0).
        width, height: int, image's width and height from x, y, use 0 for entire area.
                       If width(or height) < 0, image size will be control's width(or height) - width(or height).
        Return bool, True if succeed otherwise False.
        """
        bitmap = Bitmap()
        if bitmap.FromControl(self, x, y, width, height):
            return bitmap.ToFile(savePath)
        return False