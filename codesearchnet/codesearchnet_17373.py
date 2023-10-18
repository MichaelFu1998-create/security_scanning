def _addKeyToQueue(self, keychr, modFlags=0, globally=False):
        """Add keypress to queue.

        Parameters: key character or constant referring to a non-alpha-numeric
                    key (e.g. RETURN or TAB)
                    modifiers
                    global or app specific
        Returns: None or raise ValueError exception.
        """
        # Awkward, but makes modifier-key-only combinations possible
        # (since sendKeyWithModifiers() calls this)
        if not keychr:
            return

        if not hasattr(self, 'keyboard'):
            self.keyboard = AXKeyboard.loadKeyboard()

        if keychr in self.keyboard['upperSymbols'] and not modFlags:
            self._sendKeyWithModifiers(keychr,
                                       [AXKeyCodeConstants.SHIFT],
                                       globally)
            return

        if keychr.isupper() and not modFlags:
            self._sendKeyWithModifiers(
                keychr.lower(),
                [AXKeyCodeConstants.SHIFT],
                globally
            )
            return

        if keychr not in self.keyboard:
            self._clearEventQueue()
            raise ValueError('Key %s not found in keyboard layout' % keychr)

        # Press the key
        keyDown = Quartz.CGEventCreateKeyboardEvent(None,
                                                    self.keyboard[keychr],
                                                    True)
        # Release the key
        keyUp = Quartz.CGEventCreateKeyboardEvent(None,
                                                  self.keyboard[keychr],
                                                  False)
        # Set modflags on keyDown (default None):
        Quartz.CGEventSetFlags(keyDown, modFlags)
        # Set modflags on keyUp:
        Quartz.CGEventSetFlags(keyUp, modFlags)

        # Post the event to the given app
        if not globally:
            # To direct output to the correct application need the PSN (macOS <=10.10) or PID(macOS > 10.10):
            macVer, _, _ = platform.mac_ver()
            macVer = int(macVer.split('.')[1])
            if macVer > 10:
                appPid = self._getPid()
                self._queueEvent(Quartz.CGEventPostToPid, (appPid, keyDown))
                self._queueEvent(Quartz.CGEventPostToPid, (appPid, keyUp))
            else:
                appPsn = self._getPsnForPid(self._getPid())
                self._queueEvent(Quartz.CGEventPostToPSN, (appPsn, keyDown))
                self._queueEvent(Quartz.CGEventPostToPSN, (appPsn, keyUp))
        else:
            self._queueEvent(Quartz.CGEventPost, (0, keyDown))
            self._queueEvent(Quartz.CGEventPost, (0, keyUp))