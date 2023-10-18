def GetNextSiblingControl(self) -> 'Control':
        """
        Return `Control` subclass or None.
        """
        ele = _AutomationClient.instance().ViewWalker.GetNextSiblingElement(self.Element)
        return Control.CreateControlFromElement(ele)