def RangeFromChild(self, child) -> TextRange:
        """
        Call IUIAutomationTextPattern::RangeFromChild.
        child: `Control` or its subclass.
        Return `TextRange` or None, a text range enclosing a child element such as an image,
            hyperlink, Microsoft Excel spreadsheet, or other embedded object.
        Refer https://docs.microsoft.com/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationtextpattern-rangefromchild
        """
        textRange = self.pattern.RangeFromChild(Control.Element)
        if textRange:
            return TextRange(textRange=textRange)