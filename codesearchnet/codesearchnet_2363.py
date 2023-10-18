def GetRowHeaders(self) -> list:
        """
        Call IUIAutomationTablePattern::GetCurrentRowHeaders.
        Return list, a list of `Control` subclasses, representing all the row headers in a table.
        Refer https://docs.microsoft.com/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationtablepattern-getcurrentrowheaders
        """
        eleArray = self.pattern.GetCurrentRowHeaders()
        if eleArray:
            controls = []
            for i in range(eleArray.Length):
                ele = eleArray.GetElement(i)
                con = Control.CreateControlFromElement(element=ele)
                if con:
                    controls.append(con)
            return controls
        return []