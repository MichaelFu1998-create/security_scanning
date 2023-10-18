def GetChildren(self) -> list:
        """
        Call IUIAutomationTextRange::GetChildren.
        textAttributeId: int, a value in class `TextAttributeId`.
        Return list, a list of `Control` subclasses, embedded objects that fall within the text range..
        Refer https://docs.microsoft.com/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationtextrange-getchildren
        """
        eleArray = self.textRange.GetChildren()
        if eleArray:
            controls = []
            for i in range(eleArray.Length):
                ele = eleArray.GetElement(i)
                con = Control.CreateControlFromElement(element=ele)
                if con:
                    controls.append(con)
            return controls
        return []