def FromHandle(self, hwnd: int, left: int = 0, top: int = 0, right: int = 0, bottom: int = 0) -> bool:
        """
        Capture a native window to Bitmap by its handle.
        hwnd: int, the handle of a native window.
        left: int.
        top: int.
        right: int.
        bottom: int.
        left, top, right and bottom are control's internal postion(from 0,0).
        Return bool, True if succeed otherwise False.
        """
        self.Release()
        root = GetRootControl()
        rect = ctypes.wintypes.RECT()
        ctypes.windll.user32.GetWindowRect(hwnd, ctypes.byref(rect))
        left, top, right, bottom = left + rect.left, top + rect.top, right + rect.left, bottom + rect.top
        self._bitmap = _DllClient.instance().dll.BitmapFromWindow(root.NativeWindowHandle, left, top, right, bottom)
        self._getsize()
        return self._bitmap > 0