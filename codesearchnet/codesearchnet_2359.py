def GetItemByName(self, name: str) -> 'Control':
        """
        Call IUIAutomationSpreadsheetPattern::GetItemByName.
        name: str.
        Return `Control` subclass or None, represents the spreadsheet cell that has the specified name..
        Refer https://docs.microsoft.com/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationspreadsheetpattern-getitembyname
        """
        ele = self.pattern.GetItemByName(name)
        return Control.CreateControlFromElement(element=ele)