def GetSelection(self) -> list:
        """
        Call IUIAutomationLegacyIAccessiblePattern::GetCurrentSelection.
        Return list, a list of `Control` subclasses,
                     the Microsoft Active Accessibility property that identifies the selected children of this element.
        Refer https://docs.microsoft.com/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationlegacyiaccessiblepattern-getcurrentselection
        """
        eleArray = self.pattern.GetCurrentSelection()
        if eleArray:
            controls = []
            for i in range(eleArray.Length):
                ele = eleArray.GetElement(i)
                con = Control.CreateControlFromElement(element=ele)
                if con:
                    controls.append(con)
            return controls
        return []