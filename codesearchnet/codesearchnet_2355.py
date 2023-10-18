def SetView(self, view: int) -> bool:
        """
        Call IUIAutomationMultipleViewPattern::SetCurrentView.
        Set the view of the control.
        view: int, the control-specific view identifier.
        Return bool, True if succeed otherwise False.
        Refer https://docs.microsoft.com/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationmultipleviewpattern-getviewname
        """
        return self.pattern.SetCurrentView(view) == S_OK