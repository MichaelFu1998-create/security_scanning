def GetConversionTarget(self) -> TextRange:
        """
        Call IUIAutomationTextEditPattern::GetConversionTarget.
        Return `TextRange` or None, the current conversion target range..
        Refer https://docs.microsoft.com/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationtexteditpattern-getconversiontarget
        """
        textRange = self.pattern.GetConversionTarget()
        if textRange:
            return TextRange(textRange=textRange)