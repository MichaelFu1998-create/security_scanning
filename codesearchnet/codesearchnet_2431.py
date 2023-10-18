def SetActive(self, waitTime: float = OPERATION_WAIT_TIME) -> bool:
        """Set top level window active."""
        if self.IsTopLevel():
            handle = self.NativeWindowHandle
            if IsIconic(handle):
                ret = ShowWindow(handle, SW.Restore)
            elif not IsWindowVisible(handle):
                ret = ShowWindow(handle, SW.Show)
            ret = SetForegroundWindow(handle)  # may fail if foreground windows's process is not python
            time.sleep(waitTime)
            return ret
        return False