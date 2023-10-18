def wait(self, **kwargs):
        """Wait for the OPC to prepare itself for data transmission. On some devides this can take a few seconds
        :rtype: self
        :Example:
        >> alpha = opc.OPCN2(spi, debug=True).wait(check=200)
        >> alpha = opc.OPCN2(spi, debug=True, wait=True, check=200)
        """

        if not callable(self.on):
            raise UserWarning('Your device does not support the self.on function, try without wait')

        if not callable(self.histogram):
            raise UserWarning('Your device does not support the self.histogram function, try without wait')

        self.on()
        while True:
            try:
                if self.histogram() is None:
                    raise UserWarning('Could not load histogram, perhaps the device is not yet connected')

            except UserWarning as e:
                sleep(kwargs.get('check', 200) / 1000.)

        return self