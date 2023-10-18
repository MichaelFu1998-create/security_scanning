def Compare(self, textRange: 'TextRange') -> bool:
        """
        Call IUIAutomationTextRange::Compare.
        textRange: `TextRange`.
        Return bool, specifies whether this text range has the same endpoints as another text range.
        Refer https://docs.microsoft.com/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationtextrange-compare
        """
        return bool(self.textRange.Compare(textRange.textRange))