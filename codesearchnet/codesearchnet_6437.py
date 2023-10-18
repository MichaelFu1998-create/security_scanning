def _characteristic_changed(self, characteristic):
        """Called when the specified characteristic has changed its value."""
        # Called when a characteristic is changed.  Get the on_changed handler
        # for this characteristic (if it exists) and call it.
        on_changed = self._char_on_changed.get(characteristic, None)
        if on_changed is not None:
            on_changed(characteristic.value().bytes().tobytes())
        # Also tell the characteristic that it has a new value.
        # First get the service that is associated with this characteristic.
        char = characteristic_list().get(characteristic)
        if char is not None:
            char._value_read.set()