def GetFirstChildControl(self) -> 'Control':
        """
        Return `Control` subclass or None.
        """
        ele = _AutomationClient.instance().ViewWalker.GetFirstChildElement(self.Element)
        return Control.CreateControlFromElement(ele)