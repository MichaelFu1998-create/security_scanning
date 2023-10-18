def SetTopmost(self, isTopmost: bool = True, waitTime: float = OPERATION_WAIT_TIME) -> bool:
        """
        Set top level window topmost.
        isTopmost: bool.
        waitTime: float.
        """
        if self.IsTopLevel():
            ret = SetWindowTopmost(self.NativeWindowHandle, isTopmost)
            time.sleep(waitTime)
            return ret
        return False