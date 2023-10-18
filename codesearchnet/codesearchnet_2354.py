def SetValue(self, value: str, waitTime: float = OPERATION_WAIT_TIME) -> bool:
        """
        Call IUIAutomationLegacyIAccessiblePattern::SetValue.
        Set the Microsoft Active Accessibility value property for the element.
        value: str.
        waitTime: float.
        Return bool, True if succeed otherwise False.
        Refer https://docs.microsoft.com/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationlegacyiaccessiblepattern-setvalue
        """
        ret = self.pattern.SetValue(value) == S_OK
        time.sleep(waitTime)
        return ret