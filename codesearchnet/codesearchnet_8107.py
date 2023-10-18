def find_serial_devices(self):
        """Scan and report all compatible serial devices on system.

        :returns: List of discovered devices
        """
        if self.devices is not None:
            return self.devices

        self.devices = {}
        hardware_id = "(?i)" + self.hardware_id  # forces case insensitive

        for ports in serial.tools.list_ports.grep(hardware_id):
            port = ports[0]
            try:
                id = self.get_device_id(port)
                ver = self._get_device_version(port)
            except:
                log.debug('Error getting device_id for %s, %s',
                          port, self.baudrate)
                if True:
                    raise
                continue

            if getattr(ports, '__len__', lambda: 0)():
                log.debug('Multi-port device %s:%s:%s with %s ports found',
                          self.hardware_id, id, ver, len(ports))
            if id < 0:
                log.debug('Serial device %s:%s:%s with id %s < 0',
                          self.hardware_id, id, ver)
            else:
                self.devices[id] = port, ver

        return self.devices