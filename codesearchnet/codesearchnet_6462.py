def start_notify(self, on_change):
        """Enable notification of changes for this characteristic on the
        specified on_change callback.  on_change should be a function that takes
        one parameter which is the value (as a string of bytes) of the changed
        characteristic value.
        """
        # Tell the device what callback to use for changes to this characteristic.
        self._device._notify_characteristic(self._characteristic, on_change)
        # Turn on notifications of characteristic changes.
        self._device._peripheral.setNotifyValue_forCharacteristic_(True,
            self._characteristic)