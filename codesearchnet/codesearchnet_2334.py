def FromFile(self, filePath: str) -> bool:
        """
        Load image from a file.
        filePath: str.
        Return bool, True if succeed otherwise False.
        """
        self.Release()
        self._bitmap = _DllClient.instance().dll.BitmapFromFile(ctypes.c_wchar_p(filePath))
        self._getsize()
        return self._bitmap > 0