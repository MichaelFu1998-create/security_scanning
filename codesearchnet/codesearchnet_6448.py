def power_on(self, timeout_sec=TIMEOUT_SEC):
        """Power on Bluetooth."""
        # Turn on bluetooth and wait for powered on event to be set.
        self._powered_on.clear()
        IOBluetoothPreferenceSetControllerPowerState(1)
        if not self._powered_on.wait(timeout_sec):
            raise RuntimeError('Exceeded timeout waiting for adapter to power on!')