def SetWindowText(self, text: str) -> bool:
        """
        Call native SetWindowText if control has a valid native handle.
        """
        handle = self.NativeWindowHandle
        if handle:
            return SetWindowText(handle, text)
        return False