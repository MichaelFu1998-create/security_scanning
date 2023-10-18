def FindAttribute(self, textAttributeId: int, val, backward: bool) -> 'TextRange':
        """
        Call IUIAutomationTextRange::FindAttribute.
        textAttributeID: int, a value in class `TextAttributeId`.
        val: COM VARIANT according to textAttributeId? todo.
        backward: bool, True if the last occurring text range should be returned instead of the first; otherwise False.
        return `TextRange` or None, a text range subset that has the specified text attribute value.
        Refer https://docs.microsoft.com/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationtextrange-findattribute
        """
        textRange = self.textRange.FindAttribute(textAttributeId, val, int(backward))
        if textRange:
            return TextRange(textRange=textRange)