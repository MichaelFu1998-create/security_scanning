def checkSerial(self):
        """
        Check the serial port for data to write to the TUN adapter.
        """
        for item in self.rxSerial(self._TUN._tun.mtu):
            # print("about to send: {0}".format(item))
            try:
                self._TUN._tun.write(item)
            except pytun.Error as error:
                print("pytun error writing: {0}".format(item))
                print(error)