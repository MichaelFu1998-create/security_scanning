def GetVisibleRanges(self) -> list:
        """
        Call IUIAutomationTextPattern::GetVisibleRanges.
        Return list, a list of `TextRange`, disjoint text ranges from a text-based control
                     where each text range represents a contiguous span of visible text.
        Refer https://docs.microsoft.com/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationtextpattern-getvisibleranges
        """
        eleArray = self.pattern.GetVisibleRanges()
        if eleArray:
            textRanges = []
            for i in range(eleArray.Length):
                ele = eleArray.GetElement(i)
                textRanges.append(TextRange(textRange=ele))
            return textRanges
        return []