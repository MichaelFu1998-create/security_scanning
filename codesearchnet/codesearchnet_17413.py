def waitForWindowToDisappear(self, winName, timeout=10):
        """Convenience method to wait for a window with the given name to
        disappear.

        Returns: Boolean
        """
        callback = AXCallbacks.elemDisappearedCallback
        retelem = None
        args = (retelem, self)

        # For some reason for the AXUIElementDestroyed notification to fire,
        # we need to have a reference to it first
        win = self.findFirst(AXRole='AXWindow', AXTitle=winName)
        return self.waitFor(timeout, 'AXUIElementDestroyed',
                            callback=callback, args=args,
                            AXRole='AXWindow', AXTitle=winName)