def checkTUN(self):
        """
        Checks the TUN adapter for data and returns any that is found.

        Returns:
            packet: Data read from the TUN adapter
        """
        packet = self._TUN._tun.read(self._TUN._tun.mtu)
        return(packet)