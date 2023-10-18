def SetDockPosition(self, dockPosition: int, waitTime: float = OPERATION_WAIT_TIME) -> int:
        """
        Call IUIAutomationDockPattern::SetDockPosition.
        dockPosition: int, a value in class `DockPosition`.
        waitTime: float.
        Refer https://docs.microsoft.com/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationdockpattern-setdockposition
        """
        ret = self.pattern.SetDockPosition(dockPosition)
        time.sleep(waitTime)
        return ret