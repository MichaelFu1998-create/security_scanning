def GetActiveComposition(self) -> TextRange:
        """
        Call IUIAutomationTextEditPattern::GetActiveComposition.
        Return `TextRange` or None, the active composition.
        Refer https://docs.microsoft.com/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationtexteditpattern-getactivecomposition
        """
        textRange = self.pattern.GetActiveComposition()
        if textRange:
            return TextRange(textRange=textRange)