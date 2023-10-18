def GetPatternAs(self, patternId: int, riid):
        """
        Call IUIAutomationElement::GetCurrentPatternAs.
        Get a new pattern by pattern id if it supports the pattern, todo.
        patternId: int, a value in class `PatternId`.
        riid: GUID.
        Refer https://docs.microsoft.com/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement-getcurrentpatternas
        """
        return self.Element.GetCurrentPatternAs(patternId, riid)