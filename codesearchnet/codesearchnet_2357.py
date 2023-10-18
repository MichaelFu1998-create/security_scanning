def SetScrollPercent(self, horizontalPercent: float, verticalPercent: float, waitTime: float = OPERATION_WAIT_TIME) -> bool:
        """
        Call IUIAutomationScrollPattern::SetScrollPercent.
        Set the horizontal and vertical scroll positions as a percentage of the total content area within the UI Automation element.
        horizontalPercent: float or int, a value in [0, 100] or ScrollPattern.NoScrollValue(-1) if no scroll.
        verticalPercent: float or int, a value  in [0, 100] or ScrollPattern.NoScrollValue(-1) if no scroll.
        waitTime: float.
        Return bool, True if succeed otherwise False.
        Refer https://docs.microsoft.com/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationscrollpattern-setscrollpercent
        """
        ret = self.pattern.SetScrollPercent(horizontalPercent, verticalPercent) == S_OK
        time.sleep(waitTime)
        return ret