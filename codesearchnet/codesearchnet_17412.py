def waitForCreation(self, timeout=10, notification='AXCreated'):
        """Convenience method to wait for creation of some UI element.

        Returns: The element created
        """
        callback = AXCallbacks.returnElemCallback
        retelem = None
        args = (retelem,)

        return self.waitFor(timeout, notification, callback=callback,
                            args=args)