def _releaseModifierKeys(self, modifiers):
        """Release given modifier keys (provided in list form).

        Parameters: modifiers list
        Returns: Unsigned int representing flags to set
        """
        modFlags = self._releaseModifiers(modifiers)
        # Post the queued keypresses:
        self._postQueuedEvents()
        return modFlags