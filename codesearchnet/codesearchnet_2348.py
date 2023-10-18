def Navigate(self, direction: int) -> 'Control':
        """
        Call IUIAutomationCustomNavigationPattern::Navigate.
        Get the next control in the specified direction within the logical UI tree.
        direction: int, a value in class `NavigateDirection`.
        Return `Control` subclass or None.
        Refer https://docs.microsoft.com/en-us/windows/desktop/api/uiautomationclient/nf-uiautomationclient-iuiautomationcustomnavigationpattern-navigate
        """
        ele = self.pattern.Navigate(direction)
        return Control.CreateControlFromElement(ele)