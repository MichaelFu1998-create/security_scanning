def GetPattern(self, patternId: int):
        """
        Call IUIAutomationElement::GetCurrentPattern.
        Get a new pattern by pattern id if it supports the pattern.
        patternId: int, a value in class `PatternId`.
        Refer https://docs.microsoft.com/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationelement-getcurrentpattern
        """
        try:
            pattern = self.Element.GetCurrentPattern(patternId)
            if pattern:
                subPattern = CreatePattern(patternId, pattern)
                self._supportedPatterns[patternId] = subPattern
                return subPattern
        except comtypes.COMError as ex:
            pass