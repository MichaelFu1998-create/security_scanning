def _holdModifierKeys(self, modifiers):
        """Hold given modifier keys (provided in list form).

        Parameters: modifiers list
        Returns: Unsigned int representing flags to set
        """
        modFlags = self._pressModifiers(modifiers)
        # Post the queued keypresses:
        self._postQueuedEvents()
        return modFlags