def _sendKey(self, keychr, modFlags=0, globally=False):
        """Send one character with no modifiers.

        Parameters: key character or constant referring to a non-alpha-numeric
                    key (e.g. RETURN or TAB)
                    modifier flags,
                    global or app specific
        Returns: None or raise ValueError exception
        """
        escapedChrs = {
            '\n': AXKeyCodeConstants.RETURN,
            '\r': AXKeyCodeConstants.RETURN,
            '\t': AXKeyCodeConstants.TAB,
        }
        if keychr in escapedChrs:
            keychr = escapedChrs[keychr]

        self._addKeyToQueue(keychr, modFlags, globally=globally)
        self._postQueuedEvents()