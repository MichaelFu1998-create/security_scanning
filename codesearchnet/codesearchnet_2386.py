def WaitForInputIdle(self, milliseconds: int) -> bool:
        '''
        Call IUIAutomationWindowPattern::WaitForInputIdle.
        Cause the calling code to block for the specified time or
            until the associated process enters an idle state, whichever completes first.
        milliseconds: int.
        Return bool, True if succeed otherwise False.
        Refer https://docs.microsoft.com/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationwindowpattern-waitforinputidle
        '''
        return self.pattern.WaitForInputIdle(milliseconds) == S_OK