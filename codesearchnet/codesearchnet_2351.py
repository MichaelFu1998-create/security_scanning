def Expand(self, waitTime: float = OPERATION_WAIT_TIME) -> bool:
        """
        Call IUIAutomationExpandCollapsePattern::Expand.
        waitTime: float.
        Return bool, True if succeed otherwise False.
        Refer https://docs.microsoft.com/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationexpandcollapsepattern-collapse
        """
        ret = self.pattern.Expand() == S_OK
        time.sleep(waitTime)
        return ret