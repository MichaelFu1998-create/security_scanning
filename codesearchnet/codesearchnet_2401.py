def GetLastChildControl(self) -> 'Control':
        """
        Return `Control` subclass or None.
        """
        ele = _AutomationClient.instance().ViewWalker.GetLastChildElement(self.Element)
        return Control.CreateControlFromElement(ele)