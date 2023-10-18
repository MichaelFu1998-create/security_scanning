def get_data(self, reset_device=False):
        """
        Get data from the USB device.
        """
        try:
            if reset_device:
                self._device.reset()

            # detach kernel driver from both interfaces if attached, so we can set_configuration()
            for interface in [0,1]:
                if self._device.is_kernel_driver_active(interface):
                    LOGGER.debug('Detaching kernel driver for interface %d '
                        'of %r on ports %r', interface, self._device, self._ports)
                    self._device.detach_kernel_driver(interface)

            self._device.set_configuration()

            # Prevent kernel message:
            # "usbfs: process <PID> (python) did not claim interface x before use"
            # This will become unnecessary once pull-request #124 for
            # PyUSB has been accepted and we depend on a fixed release
            # of PyUSB.  Until then, and even with the fix applied, it
            # does not hurt to explicitly claim the interface.
            usb.util.claim_interface(self._device, INTERFACE)

                # Turns out we don't actually need that ctrl_transfer.
                # Disabling this reduces number of USBErrors from ~7/30 to 0!
                #self._device.ctrl_transfer(bmRequestType=0x21, bRequest=0x09,
                #    wValue=0x0201, wIndex=0x00, data_or_wLength='\x01\x01',
                #    timeout=TIMEOUT)


            # Magic: Our TEMPerV1.4 likes to be asked twice.  When
            # only asked once, it get's stuck on the next access and
            # requires a reset.
            self._control_transfer(COMMANDS['temp'])
            self._interrupt_read()

            # Turns out a whole lot of that magic seems unnecessary.
            #self._control_transfer(COMMANDS['ini1'])
            #self._interrupt_read()
            #self._control_transfer(COMMANDS['ini2'])
            #self._interrupt_read()
            #self._interrupt_read()

            # Get temperature
            self._control_transfer(COMMANDS['temp'])
            temp_data = self._interrupt_read()

            # Get humidity
            if self._device.product == 'TEMPer1F_H1_V1.4':
                humidity_data = temp_data
            else:
                humidity_data = None

            # Combine temperature and humidity data
            data = {'temp_data': temp_data, 'humidity_data': humidity_data}

            # Be a nice citizen and undo potential interface claiming.
            # Also see: https://github.com/walac/pyusb/blob/master/docs/tutorial.rst#dont-be-selfish
            usb.util.dispose_resources(self._device)
            return data
        except usb.USBError as err:
            if not reset_device:
                LOGGER.warning("Encountered %s, resetting %r and trying again.", err, self._device)
                return self.get_data(True)

            # Catch the permissions exception and add our message
            if "not permitted" in str(err):
                raise Exception(
                    "Permission problem accessing USB. "
                    "Maybe I need to run as root?")
            else:
                LOGGER.error(err)
                raise