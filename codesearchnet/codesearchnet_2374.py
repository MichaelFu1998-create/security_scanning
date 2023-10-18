def ScrollIntoView(self, alignTop: bool = True, waitTime: float = OPERATION_WAIT_TIME) -> bool:
        """
        Call IUIAutomationTextRange::ScrollIntoView.
        Cause the text control to scroll until the text range is visible in the viewport.
        alignTop: bool, True if the text control should be scrolled so that the text range is flush with the top of the viewport;
                        False if it should be flush with the bottom of the viewport.
        waitTime: float.
        Return bool, True if succeed otherwise False.
        Refer https://docs.microsoft.com/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationtextrange-scrollintoview
        """
        ret = self.textRange.ScrollIntoView(int(alignTop)) == S_OK
        time.sleep(waitTime)
        return ret