def disconnect_devices(self, service_uuids=[]):
        """Disconnect any connected devices that have the specified list of
        service UUIDs.  The default is an empty list which means all devices
        are disconnected.
        """
        service_uuids = set(service_uuids)
        for device in self.list_devices():
            # Skip devices that aren't connected.
            if not device.is_connected:
                continue
            device_uuids = set(map(lambda x: x.uuid, device.list_services()))
            if device_uuids >= service_uuids:
                # Found a device that has at least the requested services, now
                # disconnect from it.
                device.disconnect()