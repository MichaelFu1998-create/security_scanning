def waitForFocusToChange(self, newFocusedElem, timeout=10):
        """Convenience method to wait for focused element to change (to new
        element given).

        Returns: Boolean
        """
        return self.waitFor(timeout, 'AXFocusedUIElementChanged',
                            AXRole=newFocusedElem.AXRole,
                            AXPosition=newFocusedElem.AXPosition)