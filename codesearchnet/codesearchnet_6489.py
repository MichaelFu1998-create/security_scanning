def find_devices(self, service_uuids=[], name=None):
        """Return devices that advertise the specified service UUIDs and/or have
        the specified name.  Service_uuids should be a list of Python uuid.UUID
        objects and is optional.  Name is a string device name to look for and is
        also optional.  Will not block, instead it returns immediately with a
        list of found devices (which might be empty).
        """
        # Convert service UUID list to counter for quicker comparison.
        expected = set(service_uuids)
        # Grab all the devices.
        devices = self.list_devices()
        # Filter to just the devices that have the requested service UUID/name.
        found = []
        for device in devices:
            if name is not None:
                if device.name == name:
                    # Check if the name matches and add the device.
                    found.append(device)
            else:
                # Check if the advertised UUIDs have at least the expected UUIDs.
                actual = set(device.advertised)
                if actual >= expected:
                    found.append(device)
        return found