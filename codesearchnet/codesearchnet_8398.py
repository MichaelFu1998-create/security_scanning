def power_off(self, interval=200):
        """230v power off"""
        if self.__power_off_port is None:
            cij.err("cij.usb.relay: Invalid USB_RELAY_POWER_OFF")
            return 1

        return self.__press(self.__power_off_port, interval=interval)