def _sendKeyWithModifiers(self, keychr, modifiers, globally=False):
        """Send one character with the given modifiers pressed.

        Parameters: key character, list of modifiers, global or app specific
        Returns: None or raise ValueError exception
        """
        if not self._isSingleCharacter(keychr):
            raise ValueError('Please provide only one character to send')

        if not hasattr(self, 'keyboard'):
            self.keyboard = AXKeyboard.loadKeyboard()

        modFlags = self._pressModifiers(modifiers, globally=globally)

        # Press the non-modifier key
        self._sendKey(keychr, modFlags, globally=globally)

        # Release the modifiers
        self._releaseModifiers(modifiers, globally=globally)

        # Post the queued keypresses:
        self._postQueuedEvents()