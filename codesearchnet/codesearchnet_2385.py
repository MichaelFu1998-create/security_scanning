def SetWindowVisualState(self, state: int, waitTime: float = OPERATION_WAIT_TIME) -> bool:
        """
        Call IUIAutomationWindowPattern::SetWindowVisualState.
        Minimize, maximize, or restore the window.
        state: int, a value in class `WindowVisualState`.
        waitTime: float.
        Return bool, True if succeed otherwise False.
        Refer https://docs.microsoft.com/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationwindowpattern-setwindowvisualstate
        """
        ret = self.pattern.SetWindowVisualState(state) == S_OK
        time.sleep(waitTime)
        return ret