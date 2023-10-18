def GetPreviousSiblingControl(self) -> 'Control':
        """
        Return `Control` subclass or None.
        """
        ele = _AutomationClient.instance().ViewWalker.GetPreviousSiblingElement(self.Element)
        return Control.CreateControlFromElement(ele)