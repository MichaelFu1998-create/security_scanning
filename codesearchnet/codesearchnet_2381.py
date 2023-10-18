def Resize(self, width: int, height: int, waitTime: float = OPERATION_WAIT_TIME) -> bool:
        """
        Call IUIAutomationTransformPattern::Resize.
        Resize the UI Automation element.
        width: int.
        height: int.
        waitTime: float.
        Return bool, True if succeed otherwise False.
        Refer https://docs.microsoft.com/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationtransformpattern-resize
        """
        ret = self.pattern.Resize(width, height) == S_OK
        time.sleep(waitTime)
        return ret