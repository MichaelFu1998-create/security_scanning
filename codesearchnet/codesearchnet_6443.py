def start_notify(self, on_change):
        """Enable notification of changes for this characteristic on the
        specified on_change callback.  on_change should be a function that takes
        one parameter which is the value (as a string of bytes) of the changed
        characteristic value.
        """
        # Setup a closure to be the first step in handling the on change callback.
        # This closure will verify the characteristic is changed and pull out the
        # new value to pass to the user's on change callback.
        def characteristic_changed(iface, changed_props, invalidated_props):
            # Check that this change is for a GATT characteristic and it has a
            # new value.
            if iface != _CHARACTERISTIC_INTERFACE:
                return
            if 'Value' not in changed_props:
                return
            # Send the new value to the on_change callback.
            on_change(''.join(map(chr, changed_props['Value'])))
        # Hook up the property changed signal to call the closure above.
        self._props.connect_to_signal('PropertiesChanged', characteristic_changed)
        # Enable notifications for changes on the characteristic.
        self._characteristic.StartNotify()