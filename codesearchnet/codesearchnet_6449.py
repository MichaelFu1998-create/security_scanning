def power_off(self, timeout_sec=TIMEOUT_SEC):
        """Power off Bluetooth."""
        # Turn off bluetooth.
        self._powered_off.clear()
        IOBluetoothPreferenceSetControllerPowerState(0)
        if not self._powered_off.wait(timeout_sec):
            raise RuntimeError('Exceeded timeout waiting for adapter to power off!')