def power_on(self, interval=200):
        """230v power on"""
        if self.__power_on_port is None:
            cij.err("cij.usb.relay: Invalid USB_RELAY_POWER_ON")
            return 1

        return self.__press(self.__power_on_port, interval=interval)