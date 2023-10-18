def GetGrabbedItems(self) -> list:
        """
        Call IUIAutomationDragPattern::GetCurrentGrabbedItems.
        Return list, a list of `Control` subclasses that represent the full set of items
                     that the user is dragging as part of a drag operation.
        Refer https://docs.microsoft.com/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationdragpattern-getcurrentgrabbeditems
        """
        eleArray = self.pattern.GetCurrentGrabbedItems()
        if eleArray:
            controls = []
            for i in range(eleArray.Length):
                ele = eleArray.GetElement(i)
                con = Control.CreateControlFromElement(element=ele)
                if con:
                    controls.append(con)
            return controls
        return []