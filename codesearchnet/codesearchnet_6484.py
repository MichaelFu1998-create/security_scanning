def clear_cached_data(self):
        """Clear any internally cached BLE device data.  Necessary in some cases
        to prevent issues with stale device data getting cached by the OS.
        """
        # Go through and remove any device that isn't currently connected.
        for device in self.list_devices():
            # Skip any connected device.
            if device.is_connected:
                continue
            # Remove this device.  First get the adapter associated with the device.
            adapter = dbus.Interface(self._bus.get_object('org.bluez', device._adapter),
                                     _ADAPTER_INTERFACE)
            # Now call RemoveDevice on the adapter to remove the device from
            # bluez's DBus hierarchy.
            adapter.RemoveDevice(device._device.object_path)