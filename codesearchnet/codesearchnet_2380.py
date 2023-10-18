def Move(self, x: int, y: int, waitTime: float = OPERATION_WAIT_TIME) -> bool:
        """
        Call IUIAutomationTransformPattern::Move.
        Move the UI Automation element.
        x: int.
        y: int.
        waitTime: float.
        Return bool, True if succeed otherwise False.
        Refer https://docs.microsoft.com/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationtransformpattern-move
        """
        ret = self.pattern.Move(x, y) == S_OK
        time.sleep(waitTime)
        return ret