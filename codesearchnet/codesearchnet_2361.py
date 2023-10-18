def GetRowHeaderItems(self) -> list:
        """
        Call IUIAutomationTableItemPattern::GetCurrentRowHeaderItems.
        Return list, a list of `Control` subclasses, the row headers associated with a table item or cell.
        Refer https://docs.microsoft.com/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationtableitempattern-getcurrentrowheaderitems
        """
        eleArray = self.pattern.GetCurrentRowHeaderItems()
        if eleArray:
            controls = []
            for i in range(eleArray.Length):
                ele = eleArray.GetElement(i)
                con = Control.CreateControlFromElement(element=ele)
                if con:
                    controls.append(con)
            return controls
        return []