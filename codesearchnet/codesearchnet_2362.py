def GetColumnHeaders(self) -> list:
        """
        Call IUIAutomationTablePattern::GetCurrentColumnHeaders.
        Return list, a list of `Control` subclasses, representing all the column headers in a table..
        Refer https://docs.microsoft.com/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationtablepattern-getcurrentcolumnheaders
        """
        eleArray = self.pattern.GetCurrentColumnHeaders()
        if eleArray:
            controls = []
            for i in range(eleArray.Length):
                ele = eleArray.GetElement(i)
                con = Control.CreateControlFromElement(element=ele)
                if con:
                    controls.append(con)
            return controls
        return []