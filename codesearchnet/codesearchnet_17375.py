def _pressModifiers(self, modifiers, pressed=True, globally=False):
        """Press given modifiers (provided in list form).

        Parameters: modifiers list, global or app specific
        Optional: keypressed state (default is True (down))
        Returns: Unsigned int representing flags to set
        """
        if not isinstance(modifiers, list):
            raise TypeError('Please provide modifiers in list form')

        if not hasattr(self, 'keyboard'):
            self.keyboard = AXKeyboard.loadKeyboard()

        modFlags = 0

        # Press given modifiers
        for nextMod in modifiers:
            if nextMod not in self.keyboard:
                errStr = 'Key %s not found in keyboard layout'
                self._clearEventQueue()
                raise ValueError(errStr % self.keyboard[nextMod])
            modEvent = Quartz.CGEventCreateKeyboardEvent(
                Quartz.CGEventSourceCreate(0),
                self.keyboard[nextMod],
                pressed
            )
            if not pressed:
                # Clear the modflags:
                Quartz.CGEventSetFlags(modEvent, 0)
            if globally:
                self._queueEvent(Quartz.CGEventPost, (0, modEvent))
            else:
                # To direct output to the correct application need the PSN (macOS <=10.10) or PID(macOS > 10.10):
                macVer, _, _ = platform.mac_ver()
                macVer = int(macVer.split('.')[1])
                if macVer > 10:
                    appPid = self._getPid()
                    self._queueEvent(Quartz.CGEventPostToPid, (appPid, modEvent))
                else:
                    appPsn = self._getPsnForPid(self._getPid())
                    self._queueEvent(Quartz.CGEventPostToPSN, (appPsn, modEvent))
            # Add the modifier flags
            modFlags += AXKeyboard.modKeyFlagConstants[nextMod]

        return modFlags