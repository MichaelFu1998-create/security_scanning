def GetParentControl(self) -> 'Control':
        """
        Return `Control` subclass or None.
        """
        ele = _AutomationClient.instance().ViewWalker.GetParentElement(self.Element)
        return Control.CreateControlFromElement(ele)