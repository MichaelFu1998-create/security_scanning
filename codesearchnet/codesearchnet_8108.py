def get_device(self, id=None):
        """Returns details of either the first or specified device

        :param int id: Identifier of desired device. If not given, first device
            found will be returned

        :returns tuple: Device ID, Device Address, Firmware Version
        """
        if id is None:
            if not self.devices:
                raise ValueError('No default device for %s' % self.hardware_id)
            id, (device, version) = sorted(self.devices.items())[0]

        elif id in self.devices:
            device, version = self.devices[id]

        else:
            error = 'Unable to find device with ID %s' % id
            log.error(error)
            raise ValueError(error)

        log.info("Using COM Port: %s, Device ID: %s, Device Ver: %s",
                 device, id, version)
        return id, device, version