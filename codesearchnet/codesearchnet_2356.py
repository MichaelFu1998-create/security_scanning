def Scroll(self, horizontalAmount: int, verticalAmount: int, waitTime: float = OPERATION_WAIT_TIME) -> bool:
        """
        Call IUIAutomationScrollPattern::Scroll.
        Scroll the visible region of the content area horizontally and vertically.
        horizontalAmount: int, a value in ScrollAmount.
        verticalAmount: int, a value in ScrollAmount.
        waitTime: float.
        Return bool, True if succeed otherwise False.
        Refer https://docs.microsoft.com/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationscrollpattern-scroll
        """
        ret = self.pattern.Scroll(horizontalAmount, verticalAmount) == S_OK
        time.sleep(waitTime)
        return ret