def waitForFocusedWindowToChange(self, nextWinName, timeout=10):
        """Convenience method to wait for focused window to change

        Returns: Boolean
        """
        callback = AXCallbacks.returnElemCallback
        retelem = None
        return self.waitFor(timeout, 'AXFocusedWindowChanged',
                            AXTitle=nextWinName)