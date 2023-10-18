def set_device_brightness(self, brightness):
        """Hardware specific method to set the global brightness for
        this driver's output. This method is required to be implemented,
        however, users should call
        :py:meth:`.driver_base.DriverBase.set_brightness`
        instead of calling this method directly.

        :param int brightness: 0-255 value representing the desired
            brightness level
        """
        packet = util.generate_header(CMDTYPE.BRIGHTNESS, 1)
        packet.append(self._brightness)
        s = self._connect()
        s.sendall(packet)
        resp = ord(s.recv(1))
        return resp == RETURN_CODES.SUCCESS