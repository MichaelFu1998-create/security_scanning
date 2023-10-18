def GetColumnHeaderItems(self) -> list:
        """
        Call IUIAutomationTableItemPattern::GetCurrentColumnHeaderItems.
        Return list, a list of `Control` subclasses, the column headers associated with a table item or cell.
        Refer https://docs.microsoft.com/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationtableitempattern-getcurrentcolumnheaderitems
        """
        eleArray = self.pattern.GetCurrentColumnHeaderItems()
        if eleArray:
            controls = []
            for i in range(eleArray.Length):
                ele = eleArray.GetElement(i)
                con = Control.CreateControlFromElement(element=ele)
                if con:
                    controls.append(con)
            return controls
        return []