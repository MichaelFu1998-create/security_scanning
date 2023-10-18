def FindText(self, text: str, backward: bool, ignoreCase: bool) -> 'TextRange':
        """
        Call IUIAutomationTextRange::FindText.
        text: str,
        backward: bool, True if the last occurring text range should be returned instead of the first; otherwise False.
        ignoreCase: bool, True if case should be ignored; otherwise False.
        return `TextRange` or None, a text range subset that contains the specified text.
        Refer https://docs.microsoft.com/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationtextrange-findtext
        """
        textRange = self.textRange.FindText(text, int(backward), int(ignoreCase))
        if textRange:
            return TextRange(textRange=textRange)