def Rotate(self, degrees: int, waitTime: float = OPERATION_WAIT_TIME) -> bool:
        """
        Call IUIAutomationTransformPattern::Rotate.
        Rotates the UI Automation element.
        degrees: int.
        waitTime: float.
        Return bool, True if succeed otherwise False.
        Refer https://docs.microsoft.com/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationtransformpattern-rotate
        """
        ret = self.pattern.Rotate(degrees) == S_OK
        time.sleep(waitTime)
        return ret