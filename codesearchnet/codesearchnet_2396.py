def Element(self):
        """
        Property Element.
        Return `ctypes.POINTER(IUIAutomationElement)`.
        """
        if not self._element:
            self.Refind(maxSearchSeconds=TIME_OUT_SECOND, searchIntervalSeconds=self.searchWaitTime)
        return self._element