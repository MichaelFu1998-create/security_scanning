def RangeFromPoint(self, x: int, y: int) -> TextRange:
        """
        Call IUIAutomationTextPattern::RangeFromPoint.
        child: `Control` or its subclass.
        Return `TextRange` or None, the degenerate (empty) text range nearest to the specified screen coordinates.
        Refer https://docs.microsoft.com/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationtextpattern-rangefrompoint
        """
        textRange = self.pattern.RangeFromPoint(ctypes.wintypes.POINT(x, y))
        if textRange:
            return TextRange(textRange=textRange)