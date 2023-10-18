def GetAnnotationObjects(self) -> list:
        """
        Call IUIAutomationSelectionPattern::GetCurrentAnnotationObjects.
        Return list, a list of `Control` subclasses representing the annotations associated with this spreadsheet cell.
        Refer https://docs.microsoft.com/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationspreadsheetitempattern-getcurrentannotationobjects
        """
        eleArray = self.pattern.GetCurrentAnnotationObjects()
        if eleArray:
            controls = []
            for i in range(eleArray.Length):
                ele = eleArray.GetElement(i)
                con = Control.CreateControlFromElement(element=ele)
                if con:
                    controls.append(con)
            return controls
        return []