def ShowWindow(self, cmdShow: int, waitTime: float = OPERATION_WAIT_TIME) -> bool:
        """
        Get a native handle from self or ancestors until valid and call native `ShowWindow` with cmdShow.
        cmdShow: int, a value in in class `SW`.
        waitTime: float.
        Return bool, True if succeed otherwise False.
        """
        handle = self.NativeWindowHandle
        if not handle:
            control = self
            while not handle:
                control = control.GetParentControl()
                handle = control.NativeWindowHandle
        if handle:
            ret = ShowWindow(handle, cmdShow)
            time.sleep(waitTime)
            return ret