def ToFile(self, savePath: str) -> bool:
        """
        Save to a file.
        savePath: str, should end with .bmp, .jpg, .jpeg, .png, .gif, .tif, .tiff.
        Return bool, True if succeed otherwise False.
        """
        name, ext = os.path.splitext(savePath)
        extMap = {'.bmp': 'image/bmp'
                  , '.jpg': 'image/jpeg'
                  , '.jpeg': 'image/jpeg'
                  , '.gif': 'image/gif'
                  , '.tif': 'image/tiff'
                  , '.tiff': 'image/tiff'
                  , '.png': 'image/png'
                  }
        gdiplusImageFormat = extMap.get(ext.lower(), 'image/png')
        return bool(_DllClient.instance().dll.BitmapToFile(self._bitmap, ctypes.c_wchar_p(savePath), ctypes.c_wchar_p(gdiplusImageFormat)))