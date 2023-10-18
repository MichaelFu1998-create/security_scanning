def power_btn(self, interval=200):
        """TARGET power button"""
        if self.__power_btn_port is None:
            cij.err("cij.usb.relay: Invalid USB_RELAY_POWER_BTN")
            return 1

        return self.__press(self.__power_btn_port, interval=interval)