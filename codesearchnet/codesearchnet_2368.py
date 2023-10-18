def GetAttributeValue(self, textAttributeId: int) -> ctypes.POINTER(comtypes.IUnknown):
        """
        Call IUIAutomationTextRange::GetAttributeValue.
        textAttributeId: int, a value in class `TextAttributeId`.
        Return `ctypes.POINTER(comtypes.IUnknown)` or None, the value of the specified text attribute across the entire text range, todo.
        Refer https://docs.microsoft.com/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationtextrange-getattributevalue
        """
        return self.textRange.GetAttributeValue(textAttributeId)